from __future__ import absolute_import
from datetime import datetime
import json


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

    raise TypeError("Type not serializable")


def jsonify(input, **kwargs):
    kwargs.update({
        'default': json_serializer,
    })

    return json.dumps(input, **kwargs)
