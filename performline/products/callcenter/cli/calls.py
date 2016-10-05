from __future__ import absolute_import
import click
from ....cliutils import out


@click.group(help='Call transcripts registered for processing')
def calls():
    pass


@calls.command(help='List all calls')
@click.pass_obj
def list(state):
    out(state, state.client.calls())


@calls.command(help='Show details about a single call')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.calls(id))
