from __future__ import unicode_literals
import requests
import logging
import datetime
from .models import Model
from .responses import SuccessResponse, ErrorResponse
from .exceptions import AuthenticationFailed, \
                        NotFound, \
                        ServiceUnavailable
from .products.common.api import CommonClientMethods

ALLOWED_METHODS = ['get', 'post', 'put', 'delete', 'options', 'head']
RX_TRIM_SLASH = r'(?:^/*|/*$)'


class Client(CommonClientMethods, object):
    url = 'https://api.performmatch.com'
    prefix = '/'

    def __init__(self, token, loglevel='WARNING'):
        self.token = token

        if isinstance(loglevel, str):
            loglevel = loglevel.upper()

        lvl = logging.getLevelName(loglevel)

        if isinstance(lvl, int):
            self.loglevel = lvl
        else:
            self.loglevel = logging.INFO

        logging.basicConfig(level=self.loglevel)

    def request(self, method, path, data=None, params={}, headers={}):
        if not method.lower() in ALLOWED_METHODS:
            raise Exception('Invalid request method %s' % method)

        # add token to Authorization header
        headers['Authorization'] = 'Token %s' % self.token

        response = getattr(requests, method)(
            '%s/%s%s/' % (
                self.url.strip('/'),
                self.prefix.lstrip('/'),
                path.strip('/'),
            ),
            data=data,
            params=params,
            headers=headers)

        if response.headers.get('X-PerformLine-Deprecated') == '1':
            _notAfter = response.headers.get('X-PerformLine-Deprecated-After')
            afterMsg = ''

            if _notAfter is not None:
                notAfter = datetime.datetime.strptime(_notAfter, '%Y-%m-%dT%H:%M:%S.%f')
                afterMsg = ' It will stop working after %s. ' % notAfter

            logging.warning('The API endpoint "%s" has been marked deprecated.%s' % afterMsg)
            logging.warning((
                'Upgrade the performline Python module to the latest version to '
                'stop seeing this message.'
            ))

        if response.status_code < 400:
            return SuccessResponse(response.json())
        else:
            if response.status_code == 403:
                raise AuthenticationFailed(response.json())
            elif response.status_code == 404:
                raise NotFound(response.json())
            elif response.status_code >= 500:
                raise ServiceUnavailable(response.json())
            else:
                raise ErrorResponse(response.json())

    def wrap_response(self, response, model, flat=False):
        if isinstance(response, SuccessResponse) and response.length() > 0:
            if issubclass(model, Model):
                models = [model(i) for i in response.results()]

                if flat and len(models) == 1:
                    return models[0]
                else:
                    return models

        return None
