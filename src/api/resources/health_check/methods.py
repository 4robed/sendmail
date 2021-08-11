from src.bases.api.method_handler import MethodHandler
from src.bases.api.errors import ServiceNotAvailable, InternalServerError


class Get(MethodHandler):
    def handle_logic(self):
        return dict(success=True)
