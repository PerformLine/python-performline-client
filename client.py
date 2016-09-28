import requests
from util import *
from models import *

ALLOWED_METHODS = ['get', 'post', 'put', 'delete', 'options', 'head']

class Response:
    def __init__(self, data={}):
        self.data = data

    def status(self):
        return self.must_get('Status')

    def must_get(self, path):
        return must_get(self.data, path)

    def get(self, path, fallback=None):
        return get(self.data, path, fallback)

class SuccessResponse(Response):
    def total_length():
        return self.get('ResultCount/Total', 0)

    def length():
        return self.get('ResultCount/Current', self.total_length())

    def page_count():
        return self.get('ResultCount/Pages', 0)

    def results():
        return self.get('Results', [])


class ErrorResponse(Response):
    def message(self):
        return self.get('ErrorMessage')

    def details(self):
        return self.get('ErrorDetails')


class Client:
    url = 'https://api.performmatch.com'

    def __init__(self, token):
        self.token = token

    def request(self, method, path, data=None, params={}, headers={}):
        if not method.lower() in ALLOWED_METHODS:
            raise Exception('Invalid request method %s' % method)

        response = getattr(requests, method)(
            '/'.join([self.url.replace(r'/$', ''), path]),
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

    def brands(self, brand_id=None):
        if brand_id is None:
            response = self.request('get', '/api/common/brands/')
            return self.wrap_response(response, Brand)
        else:
            response = self.request('get', '/api/common/brands/%d/' % brand_id)
            return self.wrap_response(response, Brand, flat=True)


