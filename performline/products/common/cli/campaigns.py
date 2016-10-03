from __future__ import unicode_literals
import click


@click.group(
             help='Information on campaigns')
def campaigns():
    pass


@campaigns.command(help='List all campaigns')
@click.pass_obj
def list(state):
    click.echo(state.client.campaigns())


@campaigns.command(help='Show details about a campaign')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    state.client.campaigns(id)
