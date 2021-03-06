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
from .models import (
    Brand,
    BrandRules,
    Campaign,
    CampaignRules,
    Rule,
    TrafficSource,
    Item,
    RemediationStatus,
    Workflow
)

from ...embedded.stdlib.utils.dicts import compact


class CommonClientMethods(object):
    """Methods for retrieving data common to all products."""

    def brands(self, id=None, limit=None, offset=None, create_date=None):
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
            result = [output for output in Brand.iall(self, params=compact({
                'limit': limit,
                'offset': offset,
                'create_date': create_date,
            }))]
            if limit:
                result = result[:limit]
            return result
        else:
            return Brand.get(self, id)

    def brand_rules(self, id):
        return BrandRules.get(id)

    def campaigns(self, id=None, limit=None, offset=None, brand=None):
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
            result = [output for output in Campaign.iall(self, params=compact({
                'limit': limit,
                'offset': offset,
                'brand': brand,
            }))]
            if limit:
                result = result[:limit]
            return result
        else:
            return Campaign.get(self, id)

    def campaign_rules(self, id):
        return CampaignRules.get(id)

    def rules(self, id=None, limit=None, offset=None):
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
            result = [output for output in Rule.iall(self, params=compact({
                'limit': limit,
                'offset': offset,
            }))]
            if limit:
                result = result[:limit]
            return result
        else:
            return Rule.get(self, id)

    def trafficsources(self, id=None, limit=None, offset=None):

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
            result = [output for output in TrafficSource.iall(self, params=compact({
                'limit': limit,
                'offset': offset,
            }))]
            return result
        else:
            return TrafficSource.get(self, id)

    def items(self, id=None, limit=None, offset=None, brand=None, campaign=None):
        """
        Retrieve one or more scorable items associated with an account.

        Args:
            id (int, optional): If specified, retrieve a single item by
                the given ID.  Otherwise, return all items.

        Returns:
            An instance of :class:`~performline.products.common.models.Item`
            if ``id`` is not `None` representing the item with that ID.
            Otherwise, retrieve a list of
            :class:`~performline.products.common.models.Item` instances of all
            items associated with the account.

        Raises:
            See :func:`~performline.client.Client.request`
        """
        if id is None:
            result = [output for output in Item.iall(self, params=compact({
                'limit': limit,
                'offset': offset,
                'brand': brand,
                'campaign': campaign,
            }))]
            if limit:
                result = result[:limit]
            return result
        else:
            return Item.get(self, id)

    def remediation_statuses(self):
        """
        Retrieve all available remediation statuses available in the
        Performline platform.
        Returns:
            An instance of :class:`~performline.products.common.models.RemediationStatuses`,
            which has a property returning a list of strings representing the
            availa
        return RemediationStatus.get()
        """
    
    def workflows(self, id, product):
        return Workflow.get(id, product)
