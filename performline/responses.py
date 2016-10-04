from __future__ import unicode_literals
from __future__ import absolute_import
from .util import get, must_get


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


class ErrorResponse(Response, Exception):
    def __init__(self, data={}):
        self.data = data
        self.message = self.get('ErrorDetails', self.get('ErrorMessage'))

        super(Exception, self).__init__(self.message)
