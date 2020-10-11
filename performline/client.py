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
from .embedded.stdlib.clients.rest import StandardRestClient
from .embedded.stdlib.clients.rest.models import RestModel
from .embedded.stdlib.clients.rest.responses import SuccessResponse
from .products.common.api import CommonClientMethods
from .products.web.api import WebClientMethods
from .products.callcenter.api import CallCenterClientMethods
from .products.chatscout.api import ChatScoutClientMethods


ALLOWED_METHODS = ['get', 'post', 'put', 'delete', 'options', 'head']
RX_TRIM_SLASH = r'(?:^/*|/*$)'


class Client(
    ChatScoutClientMethods,
    CallCenterClientMethods,
    WebClientMethods,
    CommonClientMethods,
    StandardRestClient
):
    """PerformLine API Client"""

    url = 'https://api.performline.com'
    prefix = '/'

    def __init__(self, token, *args, **kwargs):
        self.headers['Authorization'] = 'Token {0}'.format(token)
        super(Client, self).__init__(*args, **kwargs)

    def wrap_response(self, response, model, flat=False):
        """
        Takes a SuccessResponse and returns the results as instances of the
        given model.

        Args:
            response (SuccessResponse): A SuccessResponse object containing the
                data to be wrapped.

            model (RestModel): A subclass of RestModel that should be used when creating
                instances for each result in the response.

            flat (bool, optional): Whether single-element lists should return
                just that element instead of the list itself.

        Returns:
            If ``response`` contains zero results, returns `None`.

            If ``response`` has one element and ``flat`` equals `True`, return the first
            element as an instance of type ``model``.

            In all other cases, return a list of instances of type ``model``.
        """

        if isinstance(response, SuccessResponse) and response.length > 0:
            if issubclass(model, RestModel):
                models = [model(self, i) for i in response.results()]

                if flat and len(models) == 1:
                    return models[0]
                else:
                    return models

        return None
