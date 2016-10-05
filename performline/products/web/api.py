from __future__ import absolute_import
from .models import WebPage


class WebClientMethods(object):
    def webpages(self, id=None):
        if id is None:
            response = self.request('get', '/web/pages/')
            return self.wrap_response(response, WebPage)
        else:
            response = self.request('get', '/web/pages/%d/' % id)
            return self.wrap_response(response, WebPage, flat=True)
