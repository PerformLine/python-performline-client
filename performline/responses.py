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
from .util import get, must_get


class Response(object):
    """
    Represents a standard API response.
    """
    def __init__(self, data={}):
        self.data = data

    def status(self):
        """
        Return the status as returned from the API.

        Returns:
            "success" or "error"
        """
        return self.must_get('Status')

    def must_get(self, path):
        """See :func:`performline.util.must_get()`"""
        return must_get(self.data, path)

    def get(self, path, fallback=None):
        """See :func:`performline.util.get()`"""
        return get(self.data, path, fallback)


class SuccessResponse(Response):
    """
    Represents a successful response from the API, including any resulting data.
    """

    def total_length(self):
        """
        Return the total length of all results that match the given query.

        Returns:
            int
        """
        return self.get('ResultCount/Total', 0)

    def length(self):
        """
        Return the length of the results in the current result set, which may be less that
        :func:`~performline.responses.total_length()` if the results were paginated.

        Returns:
            int
        """
        return self.get('ResultCount/Current', self.total_length())

    def page_count(self):
        """
        Return the number of pages in a paginated result set (if greater than 1).

        Returns:
            int
        """
        return self.get('ResultCount/Pages', 0)

    def results(self):
        """
        Returns a list of zero or more results.

        Returns:
            list
        """
        return self.get('Results', [])


class ErrorResponse(Response, Exception):
    """
    Represents an error response from the API with details about the error.
    """
    def __init__(self, data={}):
        self.data = data
        self.message = self.get('ErrorDetails', self.get('ErrorMessage'))

        super(Exception, self).__init__(self.message)
