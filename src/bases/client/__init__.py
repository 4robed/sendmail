import requests

from src.common.decorators import (request_connection_handler,
                                   request_server_error_handler)
from src.common.utils import log_data
from src.bases.error import ClientError


class Client(object):

    @request_server_error_handler(max_retry=5)
    @request_connection_handler(max_retry=5)
    def _do_request(self, method, url, timeout=5000, **kwargs):
        method_handler = getattr(requests, method, None)
        if not method_handler:
            raise ClientError('UnsupportedMethod')

        log_data(
            mode='info',
            template='{client} - REQUEST - {method} - {url} - {payload}',
            kwargs=dict(
                client=self.__class__.__name__,
                method=method,
                url=url,
                payload=kwargs
            )
        )

        response = method_handler(url=url,
                                  timeout=timeout,
                                  **kwargs)

        log_data(
            mode='info',
            template='{client} - RESPONSE - {method} - {url} - {response}',
            kwargs=dict(
                client=self.__class__.__name__,
                method=method,
                url=url,
                response=response.text
            )
        )

        return response
