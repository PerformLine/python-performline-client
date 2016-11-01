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
from .models import Brand, Campaign, Rule, TrafficSource


class CommonClientMethods(object):
    """Methods for retrieving data common to all products."""

    def brands(self, id=None, **kwargs):
        """
        Retrieve one or more brands associated with an account.

        Args:
            id (int, optional): If specified, retrieve a single brand by
                the given ID.  Otherwise, return all brands.

        Returns:
            An instance of :class:`~performline.products.common.models.Brand`
            if ``id`` is not `None` representing the brand with that ID.
            Otherwise, retrieve a list of
            :class:`~performline.products.common.models.Brand` instances of all
            brands associated with the account.

        Raises:
            See :func:`~performline.client.Client.request`
        """

        if id is None:
            instances = []

            for response in self.get_until('/common/brands/', **kwargs):
                instances.extend(self.wrap_response(response, Brand))

            return instances
        else:
            return Brand(self, {
                'Id': id,
            }).retrieve()

    def campaigns(self, id=None, **kwargs):
        """
        Retrieve one or more campaigns associated with an account.

        Args:
            id (int, optional): If specified, retrieve a single campaign by
                the given ID.  Otherwise, return all campaigns.

        Returns:
            An instance of :class:`~performline.products.common.models.Campaign`
            if ``id`` is not `None` representing the campaign with that ID.
            Otherwise, retrieve a list of
            :class:`~performline.products.common.models.Campaign` instances of all
            campaigns associated with the account.

        Raises:
            See :func:`~performline.client.Client.request`
        """

        if id is None:
            instances = []

            for response in self.get_until('/common/campaigns/', **kwargs):
                instances.extend(self.wrap_response(response, Campaign))

            return instances
        else:
            return Campaign(self, {
                'Id': id,
            }).retrieve()

    def rules(self, id=None, **kwargs):
        """
        Retrieve one or more rules associated with an account.

        Args:
            id (int, optional): If specified, retrieve a single rule by
                the given ID.  Otherwise, return all rules.

        Returns:
            An instance of :class:`~performline.products.common.models.Rule`
            if ``id`` is not `None` representing the rule with that ID.
            Otherwise, retrieve a list of
            :class:`~performline.products.common.models.Rule` instances of all
            rules associated with the account.

        Raises:
            See :func:`~performline.client.Client.request`
        """

        if id is None:
            instances = []

            for response in self.get_until('/common/rules/', **kwargs):
                instances.extend(self.wrap_response(response, Rule))

            return instances
        else:
            return Rule(self, {
                'Id': id,
            }).retrieve()

    def trafficsources(self, id=None, **kwargs):

        """
        Retrieve one or more traffic sources associated with an account.

        Args:
            id (int, optional): If specified, retrieve a single traffic source by
                the given ID.  Otherwise, return all traffic sources.

        Returns:
            An instance of :class:`~performline.products.common.models.TrafficSource`
            if ``id`` is not `None` representing the traffic source with that ID.
            Otherwise, retrieve a list of
            :class:`~performline.products.common.models.TrafficSource` instances of all
            traffic sources associated with the account.

        Raises:
            See :func:`~performline.client.Client.request`
        """
        if id is None:
            instances = []

            for response in self.get_until('/common/trafficsources/', **kwargs):
                instances.extend(self.wrap_response(response, TrafficSource))

            return instances
        else:
            return TrafficSource(self, {
                'Id': id,
            }).retrieve()
