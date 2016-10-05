from __future__ import absolute_import
import click
from ....cliutils import out


@click.group(help='Web Pages registered for processing')
def pages():
    pass


@pages.command(help='List all pages')
@click.pass_obj
def list(state):
    out(state, state.client.webpages())


@pages.command(help='Show details about a single page')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.webpages(id))
