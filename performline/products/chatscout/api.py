from __future__ import absolute_import
from .models import Chat


class ChatScoutClientMethods(object):
    def chats(self, id=None):
        if id is None:
            response = self.request('get', '/chatscout/chats/')
            return self.wrap_response(response, Chat)
        else:
            response = self.request('get', '/chatscout/chats/%d/' % id)
            return self.wrap_response(response, Chat, flat=True)
