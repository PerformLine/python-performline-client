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
"""Models representing common API objects"""
from __future__ import absolute_import

import os, json
import requests
from ...embedded.stdlib.clients.rest.models import RestModel
from ...embedded.stdlib.utils.dicts import compact

import requests
import json
import os


class Brand(RestModel):
    """
    An object for retrieving data from and working with an individual brand.
    """
    rest_root = '/common/brands/'

    def campaigns(self, limit=None, offset=None):
        return Campaign.iall(self.client, params=compact({
            'brand': self.id,
            'limit': limit,
            'offset': offset,
        }))


class BrandRules(RestModel):
    """
    An object for retrieving data rules for a specific brand.
    """
    rest_root = '/common/brands/:brand_id/rules/'

    def rules(self, limit=None, offset=None):
        return BrandRules.iall(self.client, params=compact(
            {
                'brand': self.id,
                'limit': limit,
                'offset': offset,
            }
        ))

    @staticmethod
    def get(id):
        api_key = os.environ.get("API_KEY", "Not set")
        url = "http://api.performline.com"
        rest_root = '/common/brands/' + str(id) + '/rules/'
        endpoint = url + rest_root
        headers = {
            "Authorization": "Token " + api_key
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            print("Received status code " + str(response.status_code))
            return
        content = json.loads(response._content)
        os.environ["API_KEY"] = ""
        return content["Results"]


class Campaign(RestModel):
    """
    An object for retrieving data from and working with an individual
    campaign.
    """
    rest_root = '/common/campaigns/'

    @property
    def brand(self):
        return Brand.get(self.client, self.brand_id)

    def items(self, limit=None, offset=None, brand=None):
        return Item.iall(self.client, params=compact({
            'campaign': self.id,
            'brand': brand,
            'limit': limit,
            'offset': offset,
        }))


class CampaignRules(RestModel):
    """
    An object for retrieving data rules for a specific campaign.
    """
    rest_root = 'common/campaigns/:campaign_id/rules/'

    def rules(self, limit=None, offset=None):
        return self.iall(self.client, params=compact(
            {
                'campaign': self.id,
                'limit': limit,
                'offset': offset,
            }
        ))

    @staticmethod
    def get(id):
        api_key = os.environ.get("API_KEY", "Not set")
        url = "http://api.performline.com"
        rest_root = '/common/campaigns/' + str(id) + '/rules/'
        endpoint = url + rest_root
        headers = {
            "Authorization": "Token " + api_key
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            print("Received status code " + str(response.status_code))
            return
        content = json.loads(response._content)
        os.environ["API_KEY"] = ""
        return content["Results"]


class Rule(RestModel):
    """
    An object for retrieving data from and working with an individual rule.
    """
    rest_root = '/common/rules/'


class TrafficSource(RestModel):
    """
    An object for retrieving data from and working with an individual traffic
    source.
    """
    rest_root = '/common/trafficsources/'


class Item(RestModel):
    """
    An object for retrieving data from and working with scorable content,
    regardless of product.
    """
    rest_root = '/common/items/'

    @property
    def brand(self):
        return Brand.get(self.client, self.brand_id)

    @property
    def campaign(self):
        return Campaign.get(self.client, self.campaign_id)

    @property
    def traffic_source(self):
        return TrafficSource.get(self.client, self.traffic_source_id)

class RemediationStatus(RestModel):
    """
    An object for retrieving all available remediation statuses in the 
    platform.
    """
    rest_root = "/common/remediation_status/"

    @staticmethod
    def get():
        api_key = os.environ.get("API_KEY", "Not set")
        url = "http://api.performline.com"
        rest_root = '/common/remediation_status/'
        endpoint = url + rest_root
        headers = {
            "Authorization": "Token " + api_key
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            print("Received status code " + str(response.status_code))
            return
        content = json.loads(response._content)
        os.environ["API_KEY"] = ""
        return content["Results"]["Statuses"]

class Workflow(RestModel):

    @staticmethod
    def get(id, product):
        api_key = os.environ.get("API_KEY", "Not set")
        url = "http://api.performline.com"

        if product == "web":
            product_endpoint = "/web/pages/"
        elif product == "callcenter":
            product_endpoint = "/callcenter/calls/"
        elif product == "chat":
            product_endpoint = "/chatscout/chats/"
        elif product == "social":
            product_endpoint = "/social/posts/"
        elif product == "email":
            product_endpoint = "/email/messages/"
        else:
            product_endpoint = "/common/items/"

        rest_root = product_endpoint + str(id) + '/workflow/'
        endpoint = url + rest_root
        headers = {
            "Authorization": "Token " + api_key
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            print("Received status code " + str(response.status_code))
            return
        content = json.loads(response._content)
        os.environ["API_KEY"] = ""
        return content["Results"]
