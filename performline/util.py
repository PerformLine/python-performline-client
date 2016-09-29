DATA_ELEMENT_SEPARATOR = '/'


class MissingKeyException(Exception):
    pass


def must_get(data, path):
    if not isinstance(data, dict):
        raise Exception("Response data is unavailable")

    current = data
    parts = path.split(DATA_ELEMENT_SEPARATOR)

    for i in range(0, len(parts)):
        if isinstance(current, dict) and parts[i] in current:
            current = current[parts[i]]
        else:
            raise MissingKeyException("Cannot retrieve data element '%s'", path)

    return current


def get(data, path, fallback=None):
    try:
        return must_get(data, path)
    except MissingKeyException:
        return fallback
