def autopage_fn(i, response, context):
    limit = context.params.get('limit')
    offset = response.offset or 0

    if (offset + 1) < response.total_length:
        if limit is not None:
            if isinstance(context.params.get('offset'), int):
                context.params['offset'] += limit
            else:
                context.params['offset'] = limit

            if context.params['offset'] > response.total_length:
                return True

            return False

    return True


def make_response(results,
                  status_code=200,
                  metadata=None,
                  limit=None,
                  offset=None,
                  total=None,
                  parameters={}):
    payload = {
        'StatusCode': status_code,
    }

    if status_code < 400:
        payload['Status'] = 'success'
    else:
        payload['Status'] = 'error'

    if results is not None:
        if isinstance(results, list):
            payload['Results'] = results
        else:
            payload['Results'] = [results]

        payload['ResultCount'] = {}

        if total is not None:
            payload['ResultCount']['Total'] = total
        else:
            payload['ResultCount']['Total'] = len(payload['Results'])

        if len(payload['Results']) < payload['ResultCount']['Total']:
            payload['ResultCount']['Current'] = len(payload['Results'])

        if isinstance(limit, int):
            payload['ResultCount']['Limit'] = limit
            payload['ResultCount']['Offset'] = 0

        if isinstance(offset, int):
            payload['ResultCount']['Offset'] = offset

    if isinstance(metadata, dict):
        payload['Metadata'] = metadata

    payload['Parameters'] = parameters

    return payload
