from __future__ import unicode_literals
from __future__ import absolute_import
import os
from .client import Client


def client():
    # build a test client, falling back to the well-known test API key
    c = Client(os.environ.get('PERFORMLINE_API_KEY', '00e4db7592541054d3791f42d62524f4139705c4'),
               loglevel=os.environ.get('LOGLEVEL', 'WARNING'))

    url = os.environ.get('PERFORMLINE_API_URL')
    prefix = os.environ.get('PERFORMLINE_API_PREFIX')

    if url is not None:
        c.url = url

    if prefix is not None:
        c.prefix = prefix

    return c
