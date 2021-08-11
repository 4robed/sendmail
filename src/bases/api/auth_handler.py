class AuthenticationHandler(object):
    def __init__(self, request, secret_key):
        self.request = request
        self.secret_key = secret_key

    def run(self):
        """Return User or None"""
        raise NotImplementedError
