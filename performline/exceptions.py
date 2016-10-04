from __future__ import unicode_literals
from __future__ import absolute_import
from .responses import ErrorResponse


class AuthenticationFailed(ErrorResponse):
    pass


class NotFound(ErrorResponse):
    pass


class ServiceUnavailable(ErrorResponse):
    pass
