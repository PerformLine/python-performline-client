#!/usr/bin/env python
# vim:syntax=python filetype=py
import click
from .products.common.cli.brands import brands


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
def main(api_key,
         api_host,
         api_endpoint_prefix):
    """PerformMatch Compliance API client utility"""


main.add_command(brands)
main(auto_envvar_prefix='PERFORMLINE')
