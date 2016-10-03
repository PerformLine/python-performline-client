from __future__ import unicode_literals
import click


@click.group(
             help='Information on traffic sources')
def sources():
    pass


@sources.command(help='List all traffic sources')
@click.pass_obj
def list(state):
    click.echo(state.client.trafficsources())


@sources.command(help='Show details about a traffic source')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    state.client.trafficsources(id)
