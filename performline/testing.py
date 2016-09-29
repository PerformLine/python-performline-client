import os
from client import Client


def client():
    c = Client(os.environ.get('PERFORMLINE_API_KEY'),
               loglevel=os.environ.get('LOGLEVEL', 'WARNING'))

    url = os.environ.get('PERFORMLINE_API_URL')
    prefix = os.environ.get('PERFORMLINE_API_PREFIX')

    if url is not None:
        c.url = url

    if prefix is not None:
        c.prefix = prefix

    return c
