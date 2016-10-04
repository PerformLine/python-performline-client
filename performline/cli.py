from __future__ import absolute_import
from .client import Client
from .responses import ErrorResponse
from .cliutils import errout
from .products.common.cli.brands import brands
from .products.common.cli.campaigns import campaigns
from .products.common.cli.rules import rules
from .products.common.cli.trafficsources import sources
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
              required=True,
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
main.add_command(campaigns)
main.add_command(rules)
main.add_command(sources)

try:
    main(auto_envvar_prefix='PERFORMLINE')
except Exception as e:
    if isinstance(e, ErrorResponse):
        errout('The PerformMatch API encountered an error: %s' % e.message)
    else:
        errout('Unhandled Error %s: %s' % (e.__class__.__name__, e.message))
