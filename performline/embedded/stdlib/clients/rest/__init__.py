"""
An opinionated HTTP client for consuming PerformLine internal APIs.
"""
from __future__ import absolute_import
from six import string_types
import logging
import requests
import requests_mock
import requests.exceptions
import time
import re
from datetime import datetime
import yaml
import uuid
from .responses import SuccessResponse
from .exceptions import ErrorResponse, AuthenticationFailed, NotFound, ServiceUnavailable, \
    DeprecatedEndpoint, BadGateway, TooManyIterations
from .utils import autopage_fn
from ...utils.json import jsonify
from ...utils import stats


ALLOWED_METHODS = ['get', 'post', 'put', 'delete', 'options', 'head']
RX_TRIM_SLASH = re.compile('(?:^/*|/*$)')


class RequestContext(object):
    def __init__(self, client, method, path, data=None, params={}, headers={}):
        self.client = client
        self.method = method
        self.path = path
        self.data = data
        self.params = params
        self.headers = headers


class StandardRestClient(object):
    """
    A standardized base class that can be used directly or as a subclass for consuming RESTful
    HTTP services at PerformLine.

    Args:
        url (str): The base URL that will apply to all instances of this class (can be overridden
            in subclasses)

        prefix (str): A string to prefix all paths given to the :func:`request()` method.  This is
            useful for endpoints that are always rooted at a particular path (e.g.: "/api").

        loglevel (str): A valid `logger` log level that is used for reporting details in the
            underlying HTTP library.

        content_type (str): The default MIME type that is presented to and expected from
            server responses.  This is a shorthand that populates the 'Content-Type' header by
            default.

        headers (dict): A dictionary of HTTP headers that should be included in every request. For
            example, an 'Authorization' header.

        params (dict): A dictionary of query string parameters that should be included in every
            request.  For example, `{'format': 'json'}` (which would include '?format=json' in the
            request URLs).
    """

    url = None
    prefix = '/'
    content_type = 'application/json'
    headers = {}
    params = {}
    implemented_by = None
    request_options = {}
    session = None
    models = dict()

    def __init__(
        self,
        url=None,
        prefix=None,
        loglevel='WARNING',
        content_type=None,
        params=None,
        headers=None,
        implemented_by=None,
        session=None,
        request_options={}
    ):
        # check and set the various kwargs
        for p in [
            'url',
            'prefix',
            'content_type',
            'params',
            'headers',
            'implemented_by',
            'session',
            'request_options',
        ]:
            value = locals().get(p)
            if value is not None:
                setattr(self, p, value)

        # pass along loglevel to logging module
        if isinstance(loglevel, str):
            loglevel = loglevel.upper()

        lvl = logging.getLevelName(loglevel)

        if isinstance(lvl, int):
            self.loglevel = lvl
        else:
            self.loglevel = logging.INFO

        logging.basicConfig(level=self.loglevel)

        # setup empty mock flagset
        self._mock_flags = {}

        # disables the warnings requests emits, which ARE for our own good, but if we make the
        # decision to do something stupid, we'll own that and don't need to pollute the logs.
        requests.packages.urllib3.disable_warnings()

    def request(
        self,
        method,
        path,
        data=None,
        params={},
        headers={},
        encoder='json',
        content_type=None,
        **kwargs
    ):
        """
        Perform a generic HTTP request against this instance's configured host.

        Args:
            method (str): The HTTP method to use.

            path (str): The path component of the URL for the request.

            data (any): Data to be included in the request body.

            params (dict): Query string parameters to included in the request URL.

            headers (dict): HTTP headers to include in the request.

            encoder (str, optional): If ``data`` is not None, which encoder should be used to
                pre-process the data.  A method on this client instance matching the
                format ``encode_<this value>(self,data,opts)`` will be called (see
                :func:`encode_json`, :func:`encode_yaml`). This allows for the easy implementation
                of custom encoders by defining (or overriding) methods matching this signature.
                The ``opts`` parameter will be a `dict` with keys matching some of the other
                parameters of this method (i.e.: `method`, `path`, `params`, and `headers`).  If
                this is `None`, encoding will be skipped.

            **kwargs: Additional arguments to pass directly to the underlying requests call.

        Returns:
            :class:`~performline.clients.rest.responses.SuccessResponse` if the HTTP response code
            is strictly less than 400.

        Raises:
            :class:`~performline.clients.rest.exceptions.ErrorResponse`
            :class:`~performline.clients.rest.exceptions.AuthenticationFailed`
            :class:`~performline.clients.rest.exceptions.NotFound`
            :class:`~performline.clients.rest.exceptions.ServiceUnavailable`
            :class:`~performline.clients.rest.exceptions.DeprecatedEndpoint`
        """

        if not method.lower() in ALLOWED_METHODS:
            raise Exception('Invalid request method {0}'.format(method))

        # normalize the given path
        path = path.strip('/')

        # set content type
        if self.content_type is not None:
            headers['Content-Type'] = self.content_type

        if content_type is not None:
            headers['Content-Type'] = content_type

        # merge in default headers and params
        params.update(self.params)
        headers.update(self.headers)

        for k, v in params.items():
            if v is True:
                params[k] = 'true'
            elif v is False:
                params[k] = 'false'
            else:
                params[k] = v

        # handle data encoding (if there is data to encode and we were asked to)
        if data is not None and encoder:
            try:
                encode_fn = getattr(self, 'encode_%s' % encoder)
                data = encode_fn(data, {
                    'method': method,
                    'path': path,
                    'params': params,
                    'headers': headers,
                })
            except AttributeError:
                raise AttributeError('Cannot encode data: encoder "{0}" not implemented'
                                     .format(encoder))

        # merge client-global options into the kwargs
        if isinstance(self.request_options, dict):
            kwargs.update(self.request_options)

        domain = self.url.strip('/')
        domain = domain.replace('http://', '')
        domain = domain.replace('https://', '')

        stat_tags = {
            'method': method.lower(),
            'domain': domain,
        }

        if self.implemented_by is not None:
            stat_tags['implemented_by'] = str(self.implemented_by)

        # perform the request
        try:
            stats.increment('performline.clients.rest.request', tags=stat_tags)

            with stats.time('performline.clients.rest.request.time', tags=stat_tags):
                requestor = (self.session or requests)

                response = getattr(requestor, method.lower())(
                    self.make_url(path),
                    data=data,
                    params=params,
                    headers=headers,
                    **kwargs
                )

        except requests.exceptions.SSLError:
            stats.increment('performline.clients.rest.error_ssl', tags=stat_tags)
            raise
        except requests.exceptions.ConnectionError as e:
            stats.increment('performline.clients.rest.error_on_connect', tags=stat_tags)
            raise BadGateway(
                message="Failed to connect to {}: {}".format(
                    e.request.url,
                    str(e)
                ),
                exception=e
            )

        # check for endpoint deprecation, and raise an error if the endpoint cutoff date is
        # in the past.
        try:
            _check_response_for_deprecation(path, response)
        except DeprecatedEndpoint as e:
            logging.warning((
                'Upgrade the performline Python module to the latest version to '
                'stop seeing this message.'
            ))

            if e.is_after_cutoff():
                raise

        stat_tags.update({
            'status': response.status_code,
        })

        if response.status_code < 400:
            stats.increment('performline.clients.rest.success', tags=stat_tags)
            response_body = None

            if len(response.content) > 0:
                try:
                    response_body = response.json()
                except ValueError:
                    pass

            return SuccessResponse(response, response_body)
        else:
            stats.increment('performline.clients.rest.error', tags=stat_tags)

            try:
                body = response.json()
            except ValueError:
                body = {
                    'Status': 'error',
                    'StatusCode': response.status_code,
                    'ErrorMessage': response.text,
                }

            if response.status_code == 403:
                raise AuthenticationFailed(response, body)
            elif response.status_code == 404:
                raise NotFound(response, body)
            elif response.status_code >= 500:
                raise ServiceUnavailable(response, body)
            else:
                raise ErrorResponse(response, body)

    def get(self, *args, **kwargs):
        """
        Perform a GET request.  See: :func:`request`.
        """
        return self.request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Perform a POST request.  See: :func:`request`.
        """
        return self.request('post', *args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Perform a PUT request.  See: :func:`request`.
        """
        return self.request('put', *args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Perform a DELETE request.  See: :func:`request`.
        """
        return self.request('delete', *args, **kwargs)

    def options(self, *args, **kwargs):
        """
        Perform an OPTIONS request.  See: :func:`request`.
        """
        return self.request('options', *args, **kwargs)

    def head(self, *args, **kwargs):
        """
        Perform a HEAD request.  See: :func:`request`.
        """
        return self.request('head', *args, **kwargs)

    def request_until(
        self,
        method,
        path,
        data=None,
        params={},
        headers={},
        encoder='json',
        testfn=autopage_fn,
        request_delay_ms=0,
        max_iterations=25,
        **kwargs
    ):
        """
        Perform an HTTP request repeatedly until a given function returns true.

        Args:
            See: :func:`request`

            testfn (func/lambda): A function that will be called with the signature
                ``fn(i, response, context)``; where:

                - ``i`` is the current iteration number (starting from 0)
                - ``response`` is the response for the HTTP request.
                - ``context`` (:class:`RequestContext`) is an editable request context that can
                    be used for modifying the request details for subsequent calls.

                The function should return a truthy value when request processing should stop.z

            request_delay_ms (int): The number of milliseconds to wait between successive requests
                if ``testfn`` has not evaluated to True.

            max_iterations (int): If set to a value, this is the maximum number of iterations that
                will occur before returning regardless of the output of ``testfn``.
        """

        responses = []
        count = 0
        context = RequestContext(self, method, path, data, params, headers)

        while True:
            response = self.request(
                context.method,
                context.path,
                context.data,
                context.params,
                context.headers,
                encoder,
                **kwargs
            )

            responses.append(response)

            # break if we've exceeded max_iterations
            if max_iterations is not None:
                if count >= max_iterations:
                    raise TooManyIterations(
                        "Request {} {} has exceeded the maximum iteration count of {}".format(
                            method.upper(),
                            path,
                            max_iterations
                        )
                    )

            # only loop if we were given a callable testfn
            if callable(testfn):
                # call testfn to see if we should stop now
                if testfn(count, response, context):
                    break
            else:
                break

            count += 1

            # sleep if requested
            if request_delay_ms > 0:
                time.sleep(float(request_delay_ms) / 1000.0)

        return responses

    def get_until(self, *args, **kwargs):
        """
        Perform a GET request repeatedly.  See: :func:`request_until`.
        """
        return self.request_until('get', *args, **kwargs)

    def post_until(self, *args, **kwargs):
        """
        Perform a POST request repeatedly.  See: :func:`request_until`.
        """
        return self.request_until('post', *args, **kwargs)

    def put_until(self, *args, **kwargs):
        """
        Perform a PUT request repeatedly.  See: :func:`request_until`.
        """
        return self.request_until('put', *args, **kwargs)

    def delete_until(self, *args, **kwargs):
        """
        Perform a DELETE request repeatedly.  See: :func:`request_until`.
        """
        return self.request_until('delete', *args, **kwargs)

    def options_until(self, *args, **kwargs):
        """
        Perform a OPTIONS request repeatedly.  See: :func:`request_until`.
        """
        return self.request_until('options', *args, **kwargs)

    def head_until(self, *args, **kwargs):
        """
        Perform a HEAD request repeatedly.  See: :func:`request_until`.
        """
        return self.request_until('head', *args, **kwargs)

    def make_url(self, path):
        return '{0}/{1}{2}/'.format(
            self.url.strip('/'),
            self.prefix.lstrip('/'),
            path.strip('/')
        )

    def encode_json(self, data, opts):
        """
        Returns the given data encoded as JSON

        Args:
            data (any): The data to be encoded.
            opts (dict): A dictionary populated with request context details.

        Returns:
            str
        """
        return jsonify(data)

    def encode_yaml(self, data, opts):
        """
        Returns the given data encoded as YAML

        Args:
            data (any): The data to be encoded.
            opts (dict): A dictionary populated with request context details.

        Returns:
            str
        """
        return yaml.safe_dump(data, default_flow_style=False)

    def mock_init(self, hostname=None, flags=None):
        """
        Initializes request mocking for this instance (used for testing).

        Args:
            hostname (str): Specify a specific hostname to use.
        """

        if isinstance(hostname, string_types):
            self.url = 'mock://{0}'.format(hostname)
        else:
            self.url = 'mock://{0}'.format(str(uuid.uuid4()))

        self.session = requests.Session()
        self._adapter = requests_mock.Adapter()
        self.session.mount('mock', self._adapter)

        if isinstance(flags, dict):
            self._mock_flags = flags

        return self.session

    def mock_request(self, method, path, responses, **kwargs):
        """
        Register a specific HTTP method, path, and response for this instance to respond with.

        Args:
            method (str): The HTTP method to register.

            path (str, re, func): The path (relative to this instances ``prefix``) to create a
                mock response for.  If ``path`` is a `re` regular expression, that will be used for
                matching requests directly.

                If ``path`` is a function of signature ``fn(request)``, it will be called and used
                to determine if this route should handle the request.

                See also:
                    http://requests-mock.readthedocs.io/en/latest/matching.html#custom-matching

            responses (list): A list of zero or more JSON Response payloads to include.  Responses
                will be issued in the order they are presented here; e.g.: subsequent calls to the
                same route will return the next response in the list until the list is empty.

            kwargs: Will be passed through to the underlying
                :func:`requests_mock.Adapter.request_uri` function.
        """

        if not isinstance(responses, list):
            raise AttributeError("Mock responses must be a list")

        responses = [{
            'json': r,
        } for r in responses]

        if isinstance(path, string_types):
            url = self.make_url(path)
        else:
            url = path

        logging.debug('Registering mock URL {0} {1}'.format(method, url))
        self._adapter.register_uri(method.upper(), url, responses, **kwargs)

    def mock_flag(self, key, fallback=False):
        """
        Returns the value of a flag used for mocking this service, or a fallback value if the key
        was not found.

        Args:
            key (str): The name of the flag to retrieve.

            fallback (any): The value to return if the given key is set.

        Returns:
            any
        """
        return self._mock_flags.get(key, fallback)

    def model(self, name):
        if name in self.models:
            return self.models[name]
        raise Exception('No such model "{}"'.format(name))


def _check_response_for_deprecation(path, response):
    """
    Inspects the given response's HTTP headers for a value that indicates the given path
    is deprecated.  If so, an exception will be raised.

    Args:
        path (str): The original path that was requested.

        response (:class:`requests.Response`): The HTTP response object to be inspected.

    Returns:
        None

    Raises:
        :class:`~performline.clients.rest.exceptions.DeprecatedEndpoint`
    """

    if response.headers.get('X-PerformLine-Deprecated') == '1':
        _not_after = response.headers.get('X-PerformLine-Deprecated-After')
        not_after = None
        after_msg = ''

        if _not_after is not None:
            not_after = datetime.strptime(_not_after, '%Y-%m-%dT%H:%M:%S.%f')
            after_msg = ' It will stop working after {0}. '.format(not_after)

        raise DeprecatedEndpoint('The API endpoint "{0}" has been marked deprecated.{1}'
                                 .format(path, after_msg),
                                 cutoff=not_after)
