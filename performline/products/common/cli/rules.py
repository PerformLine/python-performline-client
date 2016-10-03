from __future__ import unicode_literals
import click


@click.group(
             help='Information on rules')
def rules():
    pass


@rules.command(help='List all rules')
@click.pass_obj
def list(state):
    click.echo(state.client.rules())


@rules.command(help='Show details about a specific rule')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    state.client.rules(id)
