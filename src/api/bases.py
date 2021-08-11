from src.bases.api.resource import Resource
from src.bases.api.auth_handler import AuthenticationHandler
from src.common.utils import (
    decode_jwt_token,
)


class AuthHandler(AuthenticationHandler):
    def run(self):
        bearer_token = self.request.headers.get('Authorization', None)
        if not bearer_token:
            return None

        try:
            bearer, access_token = bearer_token.split(' ')
        except ValueError:
            return None

        if bearer != 'Bearer' or not access_token:
            return None

        token_data = decode_jwt_token(token=access_token,
                                      secret_key=self.secret_key,
                                      verify_expire=True)
        if not token_data:
            return None

        try:
            accessor_id = token_data['id']

        except Exception as error:
            print(error)
            return None

        raise Exception('need improve auth')


class BaseResource(Resource):
    auth_handler_class = AuthHandler

    auth_required = False
