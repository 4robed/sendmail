from src.bases.error import HTTPError


class Unauthorized(HTTPError):
    status_code = 401
    error = 'Unauthorized'


class MethodNotAllow(HTTPError):
    status_code = 405
    error = 'MethodNotAllow'


class BadRequestParams(HTTPError):
    status_code = 400
    error = 'BadRequestParams'


class InternalServerError(HTTPError):
    status_code = 500
    error = 'InternalServerError'


class ServiceNotAvailable(HTTPError):
    status_code = 503
    error = 'ServiceNotAvailable'
