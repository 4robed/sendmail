from src.bases.api.method_handler import MethodHandler
from src.bases.api.errors import ServiceNotAvailable, InternalServerError
from src.common.utils import log
from src.celery.task_sender import sender
from .schemas import *


class Post(MethodHandler):

    def handle_logic(self):
        # sender.send_task(
        #     name='SendMail',
        #     queue='SendMail',
        #     route_name='SendMail',
        #     kwargs=dict(
        #         template="test.html",
        #         to="loinguyenduc@vccorp.vn",
        #         subject="Xin chao",
        #         payload={},
        #     )
        # )

        return dict(success=True)
