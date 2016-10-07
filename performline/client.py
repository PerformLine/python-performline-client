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

from __future__ import unicode_literals
from __future__ import absolute_import
import requests
import logging
import datetime
from .models import Model
from .responses import SuccessResponse, ErrorResponse
from .exceptions import AuthenticationFailed, \
                        NotFound, \
                        ServiceUnavailable
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
    object
):
    """PerformLine API Client"""

    url = 'https://api.performmatch.com'
    prefix = '/'

    def __init__(self, token, loglevel='WARNING'):
        """
        Initializes a new API Client associated with a particular account.

        Args:
            token (str): The API token used to authenticate with.

            loglevel (str, optional): A Python logger level name to be used by
                the requests library (one of: 'DEBUG', 'INFO', 'WARNING',
                'ERROR').
        """
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
        """
        Performs an HTTP request against the PerformMatch API service and
        returns the results.

        Args:
            method (str): The HTTP method to use in the request (one of: 'GET'
                'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD').

            path (str): The path portion of the URL.

            data (object, optional): The data to include in the request body.

            params (dict, optional): A dict of query string parameters to include
                in the request URL.

            headers (dict, optional): A dict of HTTP headers to include in the
                request URL.

        Returns:
            A SuccessResponse instance representing a successful response.

        Raises:
            ValueError, AuthenticationFailed, NotFound, ServiceUnavailable, ErrorResponse
        """

        if not method.lower() in ALLOWED_METHODS:
            raise ValueError('Invalid request method %s' % method)

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

        if response.headers.get('X-PerformLine-Deprecated') == '1':
            _notAfter = response.headers.get('X-PerformLine-Deprecated-After')
            afterMsg = ''

            if _notAfter is not None:
                notAfter = datetime.datetime.strptime(_notAfter, '%Y-%m-%dT%H:%M:%S.%f')
                afterMsg = ' It will stop working after %s. ' % notAfter

            logging.warning('The API endpoint "%s" has been marked deprecated.%s' % afterMsg)
            logging.warning((
                'Upgrade the performline Python module to the latest version to '
                'stop seeing this message.'
            ))

        if response.status_code < 400:
            return SuccessResponse(response.json())
        else:
            if response.status_code == 403:
                raise AuthenticationFailed(response.json())
            elif response.status_code == 404:
                raise NotFound(response.json())
            elif response.status_code >= 500:
                raise ServiceUnavailable(response.json())
            else:
                raise ErrorResponse(response.json())

    def wrap_response(self, response, model, flat=False):
        """
        Takes a SuccessResponse and returns the results as instances of the
        given model.

        Args:
            response (SuccessResponse): A SuccessResponse object containing the
                data to be wrapped.

            model (Model): A subclass of Model that should be used when creating
                instances for each result in the response.

            flat (bool, optional): Whether single-element lists should return
                just that element instead of the list itself.

        Returns:
            If ``response`` contains zero results, returns `None`.

            If ``response`` has one element and ``flat`` equals `True`, return the first
            element as an instance of type ``model``.

            In all other cases, return a list of instances of type ``model``.
        """
        if isinstance(response, SuccessResponse) and response.length() > 0:
            if issubclass(model, Model):
                models = [model(i) for i in response.results()]

                if flat and len(models) == 1:
                    return models[0]
                else:
                    return models

        return None
