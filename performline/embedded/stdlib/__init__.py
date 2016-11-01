"""
PerformLine Standard Library
"""
# makes this a "namespace package"
# this must be present in the __init__.py of any "performline" package
# that overlaps with this one.
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # noqa

version = '0.6.10'
"""str: The current version of the library implementation."""
