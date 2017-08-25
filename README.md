![PerformLine](https://s3.amazonaws.com/performline-assets/images/PL_Logo_Blue-Gray_Tagline_FINAL.png "PerformLine")

# PerformLine Compliance API [![Build Status Master](https://travis-ci.com/PerformLine/python-performline-client.svg?token=3GiX3FxnBSQCxhQkAC5R&branch=master)](https://travis-ci.com/PerformLine/python-performline-client) [![PyPI](https://img.shields.io/pypi/v/performline.svg)](https://pypi.python.org/pypi/performline) [![Documentation Status](https://readthedocs.org/projects/performline/badge/?version=latest)](http://performline.readthedocs.io/en/latest/?badge=latest)

This is the Python client library and command line interface to the [PerformLine Compliance API](https://api.performline.com/).

## Documentation

Documentation for this package is located here: http://performline.readthedocs.io/en/latest/

The REST API specification and usage documentation can be found at https://api.performline.com.


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
