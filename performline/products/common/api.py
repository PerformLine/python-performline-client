from __future__ import unicode_literals
from .models import Brand, Campaign, Rule, TrafficSource


class CommonClientMethods(object):
    def brands(self, id=None):
        if id is None:
            response = self.request('get', '/common/brands/')
            return self.wrap_response(response, Brand)
        else:
            response = self.request('get', '/common/brands/%d/' % id)
            return self.wrap_response(response, Brand, flat=True)

    def campaigns(self, id=None):
        if id is None:
            response = self.request('get', '/common/campaigns/')
            return self.wrap_response(response, Campaign)
        else:
            response = self.request('get', '/common/campaigns/%d/' % id)
            return self.wrap_response(response, Campaign, flat=True)

    def rules(self, id=None):
        if id is None:
            response = self.request('get', '/common/rules/')
            return self.wrap_response(response, Rule)
        else:
            response = self.request('get', '/common/rules/%d/' % id)
            return self.wrap_response(response, Rule, flat=True)

    def trafficsources(self, id=None):
        if id is None:
            response = self.request('get', '/common/trafficsources/')
            return self.wrap_response(response, TrafficSource)
        else:
            response = self.request('get', '/common/trafficsources/%d/' % id)
            return self.wrap_response(response, TrafficSource, flat=True)
