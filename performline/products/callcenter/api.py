from __future__ import absolute_import
from .models import Call


class CallCenterClientMethods(object):
    def calls(self, id=None):
        if id is None:
            response = self.request('get', '/callcenter/calls/')
            return self.wrap_response(response, Call)
        else:
            response = self.request('get', '/callcenter/calls/%d/' % id)
            return self.wrap_response(response, Call, flat=True)
