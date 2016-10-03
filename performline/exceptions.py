from __future__ import unicode_literals
from .responses import ErrorResponse


class AuthenticationFailed(ErrorResponse):
    pass


class NotFound(ErrorResponse):
    pass


class ServiceUnavailable(ErrorResponse):
    pass
