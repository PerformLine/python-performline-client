from __future__ import absolute_import
import click
from ....cliutils import out


@click.group(help='Chats registered for processing')
def chats():
    pass


@chats.command(help='List all chats')
@click.pass_obj
def list(state):
    out(state, state.client.chats())


@chats.command(help='Show details about a single chat')
@click.argument('id',
                type=int)
@click.pass_obj
def show(state, id):
    out(state, state.client.chats(id))
