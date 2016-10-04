import click
from ....cliutils import out


@click.group(help='Information on campaigns')
def campaigns():
    pass


@campaigns.command(help='List all campaigns')
@click.pass_obj
def list(state):
    out(state, state.client.campaigns())


@campaigns.command(help='Show details about a campaign')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.campaigns(id))
