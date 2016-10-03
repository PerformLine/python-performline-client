#!/usr/bin/env python
# vim:syntax=python filetype=py
from __future__ import unicode_literals
from .client import Client
from .products.common.cli.brands import brands
from .products.common.cli.campaigns import campaigns
from .products.common.cli.rules import rules
from .products.common.cli.trafficsources import sources
import click
import os
import sys


def errout(message, exitcode=1):
    sys.stderr.write('%s\n' % message)
    os.exit(exitcode)


class State(object):
    def __init__(self, options={}):
        self.token = options.get('token')
        self.url = options.get('url')
        self.prefix = options.get('prefix')
        self.loglevel = options.get('loglevel')

        if self.loglevel is not None:
            self.client = Client(self.token, loglevel=self.loglevel)
        else:
            self.client = Client(self.token)

        if self.url:
            self.client.url = self.url

        if self.prefix:
            self.client.prefix = self.prefix


@click.group()
@click.option('--api-key', '-k',
              metavar='KEY',
              help='The API key to use for authentication',
              required=True,
              envvar='API_KEY')
@click.option('--api-host',
              metavar='URL',
              help=(
                  'The URL to use to connect to the PerformMatch API service '
                  '(this should normally not need to be changed)'
              ),
              envvar='API_URL')
@click.option('--api-endpoint-prefix',
              metavar='PATH',
              help=(
                  'A string to prefix API endpoint paths with'
                  '(this should normally not need to be changed)'
              ),
              envvar='API_PREFIX')
@click.option('--log-level', '-L',
              default='warning',
              type=click.Choice([
                'debug', 'info', 'warning', 'error',
              ]),
              envvar='LOGLEVEL')
@click.option('--format', '-f',
              default='text',
              type=click.Choice([
                'text', 'json', 'yaml',
              ]))
@click.pass_context
def main(ctx,
         api_key,
         api_host,
         api_endpoint_prefix,
         log_level,
         format):
    """PerformMatch Compliance API client utility"""
    ctx.obj = State({
        'token':    api_key,
        'url':      api_host,
        'prefix':   api_endpoint_prefix,
        'loglevel': log_level,
    })

main.add_command(brands)
main.add_command(campaigns)
main.add_command(rules)
main.add_command(sources)
main(auto_envvar_prefix='PERFORMLINE')
