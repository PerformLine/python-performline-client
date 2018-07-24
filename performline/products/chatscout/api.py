# Copyright (c) 2016, PerformLine, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the company nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PERFORMLINE, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import
from .models import Chat
from ...embedded.stdlib.utils.dicts import compact


class ChatScoutClientMethods(object):
    """Methods for retrieving data from the ChatScout product"""

    def chats(self, id=None, limit=None, offset=None, brand=None, campaign=None):
        """
        Retrieve one or more chats associated with an account.

        Args:
            id (int, optional): If specified, retrieve a single chat by
                the given ID.  Otherwise, return all chats.

        Returns:
            An instance of :class:`~performline.products.chatscout.models.Chat`
            if ``id`` is not `None` representing the chat with that ID.
            Otherwise, retrieve a list of
            :class:`~performline.products.chatscout.models.Chat` instances of all
            chats associated with the account.

        Raises:
            See :func:`~performline.client.Client.request`
        """
        if id is None:
            return Chat.iall(self, params=compact({
                'limit': limit,
                'offset': offset,
                'brand': brand,
                'campaign': campaign,                
            }))
        else:
            return Chat.get(self, id)
