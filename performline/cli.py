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
from .client import Client
from .responses import ErrorResponse
from .cliutils import errout
from .products.common.cli.brands import brands
from .products.common.cli.campaigns import campaigns
from .products.common.cli.rules import rules
from .products.common.cli.trafficsources import sources
from .products.web.cli.pages import pages
from .products.callcenter.cli.calls import calls
from .products.chatscout.cli.chats import chats
import click


class State(object):
    def __init__(self, context, options={}):
        self.context = context
        self.token = options.get('token')
        self.url = options.get('url')
        self.prefix = options.get('prefix')
        self.loglevel = options.get('loglevel')
        self.fmt = options.get('format')

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
              help=(
                'The API key to use for authentication '
                '[$PERFORMLINE_API_KEY]'
              ),
              envvar='API_KEY')
@click.option('--api-host',
              metavar='URL',
              help=(
                  'The URL to use to connect to the PerformMatch API service '
                  '(this should normally not need to be changed)\n'
                  '[$PERFORMLINE_API_URL]'
              ),
              envvar='API_URL')
@click.option('--api-endpoint-prefix',
              metavar='PATH',
              help=(
                  'A string to prefix API endpoint paths with '
                  '(this should normally not need to be changed)\n'
                  '[$PERFORMLINE_API_PREFIX]'
              ),
              envvar='API_PREFIX')
@click.option('--log-level', '-L',
              default='warning',
              help=(
                  'Set the level of logging verbosity\n'
                  '[$PERFORMLINE_LOGLEVEL]'
              ),
              type=click.Choice([
                'debug', 'info', 'warning', 'error',
              ]),
              envvar='LOGLEVEL')
@click.option('--format', '-f',
              default='yaml',
              type=click.Choice([
                'yaml', 'json',
              ]))
@click.pass_context
def main(ctx,
         api_key,
         api_host,
         api_endpoint_prefix,
         log_level,
         format):
    """PerformMatch Compliance API client utility"""
    ctx.obj = State(ctx, {
        'token': api_key,
        'url': api_host,
        'prefix': api_endpoint_prefix,
        'loglevel': log_level,
        'format': format,
    })

main.add_command(brands)
main.add_command(calls)
main.add_command(campaigns)
main.add_command(chats)
main.add_command(pages)
main.add_command(rules)
main.add_command(sources)

try:
    main(auto_envvar_prefix='PERFORMLINE')
except Exception as e:
    if isinstance(e, ErrorResponse):
        errout('The PerformMatch API encountered an error: %s' % e.message)
    else:
        errout('Unhandled Error %s: %s' % (e.__class__.__name__, e.message))
