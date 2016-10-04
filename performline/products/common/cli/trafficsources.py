import click
from ....cliutils import out


@click.group(help='Information on traffic sources')
def sources():
    pass


@sources.command(help='List all traffic sources')
@click.pass_obj
def list(state):
    out(state, state.client.trafficsources())


@sources.command(help='Show details about a traffic source')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.trafficsources(id))
