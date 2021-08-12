from src.bases.schema import BaseSchema
from src.bases.error import HTTPError


class PayloadHandler(object):
    def __init__(self, request):
        self.request = request

    def fetch(self):
        if self.request.method in ['GET', 'DELETE']:
            payload = self.request.args or {}
        else:
            payload = self.request.json or {}
        return payload.copy()


class MethodHandler(object):
    # HTTP method authentication toggle
    auth_required = False

    send_file = False

    permission_requirements = None

    input_schema_class = BaseSchema

    payload_handler = PayloadHandler

    raw_params = None

    # request payload
    payload = None

    # indicate this method will redirect after doing its logic
    redirect = False

    # indicate which keys will be returned in the result data,
    # empty means all keys.
    output_keys = []

    def __init__(self,
                 app,
                 request,
                 accessor=None,
                 redis=None):

        self.app = app
        self.request = request
        self.accessor = accessor
        self.redis = redis

        self._check_auth()

        self._check_permission()

        self.raw_params = self._get_raw_params()

        self.output_keys = self._get_output_keys()

        self.payload = self._parse_raw_params()

    def _get_raw_params(self):
        handler = self.payload_handler(request=self.request)
        return handler.fetch()

    def handle_logic(self):
        """The main logic of this HTTP method"""
        raise NotImplementedError

    def handle_output(self, data):
        if self.redirect:
            if not isinstance(data, str):
                raise Exception('output must be a str URL for redirection')
        if self.send_file:
            if not isinstance(data, str):
                raise Exception('output must be a str path of file')
        return data

    def _parse_raw_params(self):
        schema = self.input_schema_class(unknown='EXCLUDE')

        err = schema.validate(self.raw_params)
        if err:
            raise HTTPError(message=str(err),
                            error='BadRequestParams',
                            status_code=400)
        result = schema.load(self.raw_params)

        result['language_code'] = self.request.headers.get('Accept-Language') or 'vi'
        return result

    def _check_auth(self):
        if self.auth_required and not self.accessor:
            raise HTTPError(error='Unauthorized',
                            status_code=401)

    def _check_permission(self):
        if not self.permission_requirements:
            return

        # role_service = RoleService(self.session)
        # if not role_service.check_permissions(
        #     roles=self.accessor.roles,
        #     perm_requirements=self.permission_requirements
        # ):
        #     raise PermissionError

    def _get_output_keys(self):
        return self.raw_params.get('output_keys') or []

    def run(self):
        """The main flow of this HTTP method"""

        # handle logic
        result = self.handle_logic()

        # handle output
        output = self.handle_output(result)

        return output

