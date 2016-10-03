from __future__ import unicode_literals
import click


@click.group(
             help='Brands associated with your account')
def brands():
    pass


@brands.command(help='List all brands')
@click.pass_obj
def list(state):
    click.echo(state.client.brands())


@brands.command(help='Show details about a single brand')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    state.client.brands(id)
