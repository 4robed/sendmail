from src.api.bases import BaseResource


class TestResource(BaseResource):
    auth_required = False
    endpoint = '/test'
