from __future__ import absolute_import
import click
import sys
import json
import yaml


def normalize(data):
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    elif isinstance(data, list):
        if len(data) > 0:
            data = [normalize(i) for i in data]

    return data


def errout(message, exitcode=1):
    sys.stderr.write('%s\n' % message)
    exit(exitcode)


def out(state, data=None):
    rv = ''
    data = normalize(data)

    if data is None:
        return

    if state.fmt == 'json':
        rv = json.dumps(data, indent=4)
    elif state.fmt == 'yaml':
        rv = yaml.safe_dump(data, default_flow_style=False)
    else:
        rv = str(data)

    if len(rv) > 0:
        click.echo(rv)
