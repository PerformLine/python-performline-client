import click
from ....cliutils import out


@click.group(help='Information on rules')
def rules():
    pass


@rules.command(help='List all rules')
@click.pass_obj
def list(state):
    out(state, state.client.rules())


@rules.command(help='Show details about a specific rule')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.rules(id))
