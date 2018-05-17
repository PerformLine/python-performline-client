from __future__ import absolute_import
from six import string_types
import math
import json
from ...utils.dicts import deep_get, must_deep_get


class Response(object):
    """
    A base class that provides common accessors for all standard REST responses (successful or
    erroneous).  Normally, this class is not created directly, but is instead returned (usually
    subclassed) by :func:`~performline.clients.rest.StandardRestClient.request`.

    Args:
        response (:class:`requests.Response`): The response object from the underlying HTTP
            library.

        data (dict): The decoded response payload matching the standard REST response format.
    """

    def __init__(self, response, data={}):
        self.response = response
        self._payload = data

    @property
    def payload(self):
        """
        Attempts to retrieve an arbitrary payload from the embedded response data.  If the embedded
        data is a string, attempt to JSON decode it, but fallback to just returning the data as-is.

        If the cached value exists and is not none, return it.

        In all other cases, return None.

        Returns:
            The embedded payload as a decoded JSON value (list, dict), the data value as-is,
            or `None`.
        """
        if hasattr(self, '_payload') and self._payload is not None:
            return self._payload
        elif hasattr(self, 'data'):
            if isinstance(self.data, (string_types, bytes)):
                try:
                    self._payload = json.loads(self.data)
                except ValueError:
                    self._payload = self.data
            else:
                self._payload = self.data

            return self._payload

        return None

    def clear_payload(self):
        """
        Clears the internal cached payload object
        """
        self._payload = None

    @property
    def status_code(self):
        """
        Returns the HTTP status code embedded in the response payload.

        Returns:
            int
        """

        if self.response:
            fallback = self.response.status_code
        else:
            fallback = None

        return self.deep_get('StatusCode', fallback)

    @property
    def response_status(self):
        """
        Returns the response status as described in the standard REST 'Status' field.

        Returns:
            str; "success" or "error"
        """
        return self.must_deep_get('Status')

    @property
    def metadata(self):
        """
        Returns any metadata included in the response object.

        Returns:
            dict
        """
        return self.deep_get('Metadata', {})

    def metadata_get(self, key, fallback=None):
        """
        Returns a deeply nested value from the metadata object, or a fallback value if not present.

        Args:
            key (str): The path to the value to retrieve.

            fallback (any, optional): A value to return if required is False and the key isn't
                present.

        Returns:
            any
        """
        return deep_get(self.metadata, key, fallback)

    def haserror(self):
        """
        Shorthand for checking if the status is erroneous.

        Returns:
            bool
        """
        return (self.deep_get('Status') == 'error')

    def must_deep_get(self, path):
        """
        See: :func:`performline.utils.dicts.must_deep_get`
        """
        return must_deep_get(self.payload, path)

    def deep_get(self, path, fallback=None):
        """
        See: :func:`performline.utils.dicts.deep_get`
        """
        return deep_get(self.payload, path, fallback)

    def get(self, key, fallback=None):
        return self.deep_get(key, fallback)


class SuccessResponse(Response):
    """
    A subclass of :class:`Response` that provides accessors for fields present in successful REST
    responses.
    """
    @property
    def total_length(self):
        """
        Return the total number of results in a multi-valued result set.

        Returns:
            int
        """
        return self.deep_get('ResultCount/Total', 0)

    @property
    def length(self):
        """
        Return the number of results in the current response, which may be less than
             :func:`total_length` in a paginated result set.

        Returns:
            int
        """
        return self.deep_get('ResultCount/Current', self.total_length)

    @property
    def limit(self):
        """
        Return the number of results per page.

        Returns:
            int
        """
        return self.deep_get('ResultCount/Limit', self.length)

    @property
    def offset(self):
        """
        Return the number of results the results list is offset from the beginning of
        the total resultset.

        Returns:
            int
        """
        return self.deep_get('ResultCount/Offset', 0)

    @property
    def total_pages(self):
        """
        Return the total number of pages that contain the full result set.

        Returns:
            int
        """
        if self.limit == 0:
            return 0
        else:
            return int(math.ceil(float(self.total_length) / float(self.limit)))

    @property
    def current_page(self):
        """
        Return the current page number in a paginated result set (starting with
        page 1).

        Returns:
            int
        """

        if self.offset == 0:
            return 1
        else:
            return int(float(self.offset) / float(self.limit)) + 1

    def results(self, index=None):
        """
        Return results from a standard REST response.

        Returns:
            list, dict (if ``index`` was specified)
        """
        results = self.deep_get('Results', [])

        if results is None:
            return []

        if not isinstance(results, list):
            results = [results]

        if index is not None:
            if index < len(results):
                return results[index]
            else:
                return {}
        else:
            return results

    def results_get(self, key, fallback=None, flatten=False, required=False):
        """
        Retrieves a given value from each element in the Results response.

        Args:
            key (str): The path to the value to retrieve.

            fallback (any, optional): A value to return if required is False and the key isn't
                present.

            required (bool, optional): Whether to raise an exception if the key isn't present in
                any list element.

            flatten (bool, optional): If True, return None for empty results, and return the first
                list element if the result list has a single element, otherwise return the list.

        Returns:
            list, None, any

        Raises:
            :class:`~performline.utils.dicts.MissingKeyException`
        """

        values = []

        for result in self.deep_get('Results', []):
            if isinstance(result, dict):
                if required:
                    values.append(must_deep_get(result, key))
                else:
                    values.append(deep_get(result, key, fallback))

        if flatten:
            if len(values) == 0:
                return fallback
            elif len(values) == 1:
                return values[0]

        return values
