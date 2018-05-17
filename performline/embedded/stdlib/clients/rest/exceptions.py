from __future__ import absolute_import
from datetime import datetime
from .responses import Response
from ...utils.dicts import deep_get


class TooManyIterations(Exception):
    pass


class UnsupportedOperation(Exception):
    pass


class ErrorResponse(Response, Exception):
    """
    A subclass of :class:`~performline.clients.rest.responses.Response` that provides accessors for
    fields present in erroneous REST responses.  It is also a subclass of :class:`Exception` and
    can be raised as such.
    """
    data = {}

    def __init__(self, response=None, data=None, exception=None, message=None):
        self.response = response
        self.data = (data or {})
        self.exception = exception

        if message is not None:
            self.message = message
        else:
            err_message = None
            err_details = None

            try:
                err_message = deep_get(self.data, 'ErrorMessage', '')
            except:
                pass

            try:
                err_details = deep_get(self.data, 'ErrorDetails', '')
            except:
                pass

            self.message = 'HTTP Request Error:\n' + "\n".join([
                'Message:   {0}'.format(str(err_message)),
                'Details:   {0}'.format(str(err_details)),
                'Response:  {0}'.format(str(self.response)),
                'Body:      {0}'.format(str(self.data)),
                'Exception: {0}'.format(str(self.exception)),
            ])

        super(Exception, self).__init__(self.message)


class AuthenticationFailed(ErrorResponse):
    """
    An error condition indicating that the provided API key is not authorized to access
    a given resource.
    """
    code = 403
    data = {
        'Status': 'error',
        'StatusCode': 403,
    }


class NotFound(ErrorResponse):
    """
    An error condition indicating that the requested resource does not exist.
    """
    code = 404
    data = {
        'Status': 'error',
        'StatusCode': 404,
    }


class ServiceUnavailable(ErrorResponse):
    """
    An error condition indicating that the API service is temporarily unavailable.
    """
    code = 503
    data = {
        'Status': 'error',
        'StatusCode': 503,
    }


class UninitializedClient(Exception):
    """
    Indicates that a client instance is required to perform an operation, but one was not provided.
    """
    pass


class DeprecatedEndpoint(ErrorResponse):
    """
    Indicates that the requested endpoint is deprecated and should not be used.
    """
    code = 410
    data = {
        'Status': 'error',
        'StatusCode': 410,
    }

    def __init__(self, message, cutoff=None):
        self._cutoff = cutoff
        super(Exception, self).__init__(message)

    @property
    def cutoff(self):
        return self._cutoff

    def is_after_cutoff(self):
        """
        Returns whether the current UTC time is after the cutoff time (if available).

        Returns:
            bool
        """
        if self.cutoff:
            if datetime.utcnow() > self.cutoff:
                return True

        return False


class BadGateway(ErrorResponse):
    """
    Indicates an error message from an upstream service.
    """
    code = 502
    data = {
        'Status': 'error',
        'StatusCode': 502,
    }
