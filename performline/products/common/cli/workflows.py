# Copyright (c) 2016, PerformLine, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the company nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PERFORMLINE, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import
import click
from ....cliutils import out


@click.group(help='All workflows in the Performline platform')
def workflows():
    pass


@workflows.command(help='List all workflows for a given item')
@click.argument('id',
                type=int)
@click.pass_obj
def common(state, id):
    out(state, state.client.workflows(id, "common"))


@workflows.command(help='List all workflows for a given item')
@click.argument('id',
                type=int)
@click.pass_obj
def web(state, id):
    out(state, state.client.workflows(id, "web"))


@workflows.command(help='List all workflows for a given item')
@click.argument('id',
                type=int)
@click.pass_obj
def calls(state, id):
    out(state, state.client.workflows(id, "calls"))


@workflows.command(help='List all workflows for a given item')
@click.argument('id',
                type=int)
@click.pass_obj
def chat(state, id):
    out(state, state.client.workflows(id, "chat"))


@workflows.command(help='List all workflows for a given item')
@click.argument('id',
                type=int)
@click.pass_obj
def social(state, id):
    out(state, state.client.workflows(id, "social"))


@workflows.command(help='List all workflows for a given item')
@click.argument('id',
                type=int)
@click.pass_obj
def email(state, id):
    out(state, state.client.workflows(id, "email"))