from __future__ import unicode_literals
from __future__ import absolute_import
from .util import must_get, camelize


class Model(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        candidate_key = camelize(name, True)

        if candidate_key in self.data:
            return must_get(self.data, candidate_key)
        else:
            return super(self, name)

    def to_dict(self):
        return self.data
