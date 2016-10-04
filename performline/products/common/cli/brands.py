from __future__ import absolute_import
import click
from ....cliutils import out


@click.group(help='Brands associated with your account')
def brands():
    pass


@brands.command(help='List all brands')
@click.pass_obj
def list(state):
    out(state, state.client.brands())


@brands.command(help='Show details about a single brand')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.brands(id))
