from src.api.bases import BaseResource


class HealthCheckResource(BaseResource):
    auth_required = False
    endpoint = '/health-check'
