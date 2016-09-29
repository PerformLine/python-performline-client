import requests
import logging
from util import get, must_get
from models import Model
from .products.common.api import CommonClientMethods

ALLOWED_METHODS = ['get', 'post', 'put', 'delete', 'options', 'head']
RX_TRIM_SLASH = r'(?:^/*|/*$)'


class Response(object):
    def __init__(self, data={}):
        self.data = data

    def status(self):
        return self.must_get('Status')

    def must_get(self, path):
        return must_get(self.data, path)

    def get(self, path, fallback=None):
        return get(self.data, path, fallback)


class SuccessResponse(Response):
    def total_length(self):
        return self.get('ResultCount/Total', 0)

    def length(self):
        return self.get('ResultCount/Current', self.total_length())

    def page_count(self):
        return self.get('ResultCount/Pages', 0)

    def results(self):
        return self.get('Results', [])


class ErrorResponse(Response):
    def message(self):
        return self.get('ErrorMessage')

    def details(self):
        return self.get('ErrorDetails')


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

        if response.status_code < 400:
            return SuccessResponse(response.json())
        else:
            return ErrorResponse(response.json())

    def wrap_response(self, response, model, flat=False):
        if isinstance(response, ErrorResponse):
            raise Exception(response.message())
        elif isinstance(response, SuccessResponse) and response.length() > 0:
            if isinstance(model, Model):
                models = [Model(i) for i in response.results()]

                if flat and len(models) == 1:
                    return models[0]
                else:
                    return models

        return None
