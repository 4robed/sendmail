import json


class BaseError(Exception):
    error = None
    message = 'An unknown error happened.'

    def __init__(self,
                 error: str = None,
                 message: str = None,
                 meta: dict = None):

        if message:
            self.message = message

        if not error:
            self.error = self.__class__.__name__
        else:
            self.error = error

        self.meta = meta or {}

    def output(self) -> dict:
        data = {
            'message': self.message,
            'error': self.error,
            'meta': self.meta
        }
        return data

    def __str__(self):
        return json.dumps(self.output())


class HTTPError(BaseError):
    status_code = 500
    message = None

    def __init__(self,
                 error=None,
                 status_code=None,
                 *args, **kwargs):
        if status_code:
            self.status_code = status_code
        super(HTTPError, self).__init__(error=error,
                                        *args, **kwargs)

    def output(self):
        result = super(HTTPError, self).output()
        result['status_code'] = self.status_code
        return result


class ServiceError(BaseError):
    pass


class ClientError(BaseError):
    pass
