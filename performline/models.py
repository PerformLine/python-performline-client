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
from .util import must_get, get, camelize
from .exceptions import UninitializedClient


class Model(object):
    """
    Generic representation of a successful API response object that allows
    for straightforward access to object fields as attributes, serializing the
    object as a dictionary, or performing additional work on the object via the
    provided client instance.
    """

    def __init__(self, data, client=None):
        """
        Instantiate a new model instance populated with the given data and associated
        with a given client.

        Args:
            data (dict): A dictionary representing the data that should be accessible on this
                object.

            client (:class:`performline.client.Client`, optional): An instance of a API Client that
                can be used for loading data associated with this model instance.
        """
        self.data = data
        self._client = client

    @property
    def client(self):
        """
        Retrieve the client instance that was used when creating this model instance.

        Returns:
            :class:`performline.client.Client`

        Raises:
            UninitializedClient if the client was not provided.
        """
        if self._client is not None:
            return self._client
        else:
            raise UninitializedClient("Client not initialized")

    def get(self, key, fallback=None):
        """
        Retrieve a value from the model's instance data directly, or return the given fallback
        value if the key is not present.  ``key`` can also retrieve values in nested dictionaries
        by specifying it as a slash (/) separated path;

        e.g.: "path/to/key" would return 1.5 from the following dict:

        {
            "path": {
                "to": {
                    "key": 1.5,
                },
            },
        }

        Returns:
            The value pointed to by ``path``, or ``fallback`` if the key (or any intermediary key)
            does not exist.
        """
        return get(self.data, key, fallback)

    def __getattr__(self, name):
        """
        Facilitates retrieving values from this model as attributes on the object.  Deeply nested
        values can be accessed by specifying the path with double-underscore (__) separators.  If
        the attribute-turned-key does not exist, call the superclass attribute as usual.

        e.g.: path__to__key would return 1.5 from the following model data dict:

        {
            "path": {
                "to": {
                    "key": 1.5,
                },
            },
        }

        """

        # how to handle attribute accessors:
        # 1. split the attribute name on "__"
        # 2. camelize each element in that list
        # 3. join those elements on slash (/)
        #
        candidate_key = '/'.join([camelize(n, True) for n in name.split('__')])

        if candidate_key in self.data:
            return must_get(self.data, candidate_key)
        else:
            return super(self, name)

    def to_dict(self):
        """
        Return the embedded data dictionary directly.
        """
        return self.data
