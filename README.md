![PerformMatch](https://performmatch.com/static/images/login/PM_logo-dark-blue.png "PerformMatch")

# PerformMatch Compliance API [![Build Status Master](https://travis-ci.com/PerformLine/python-performline-client.svg?token=3GiX3FxnBSQCxhQkAC5R&branch=master)](https://travis-ci.com/PerformLine/python-performline-client) [![PyPI](https://img.shields.io/pypi/v/performline.svg)](https://pypi.python.org/pypi/performline)

This is the Python client library and command line interface to the [PerformMatch Compliance API](https://api.performmatch.com/).

## Documentation

Documentation for this package is located here: _TODO_

The REST API specification and usage documentation can be found at https://api.performmatch.com.


## Quickstart

### Basic command line to list all brands on your account

```bash
pip install performline
performline -k <API KEY> brands list
```

### Basic Python script to list all brands on your account

```python
from performline.client import Client

c = Client("<API KEY>")

for brand in c.brands():
    print("brand id=%d name=%s" % (brand.id, brand.name))


```

## Useful Details

* The API key is required for the command line utility to work, and can be specified either in the
  command invocation using the `-k/--api-key` flags or using the `$PERFORMLINE_API_KEY` environment
  variable.

* The command line utility defaults to outputting results in YAML format, but can also emit JSON with
  the `-f/--format json` flag.  This is very useful in tandem with the [jq](https://stedolan.github.io/jq/)
  utility for scripting.


## License

See [LICENSE](LICENSE) file.
