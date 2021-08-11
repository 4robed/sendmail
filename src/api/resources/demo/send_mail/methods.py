from src.bases.api.method_handler import MethodHandler
from src.bases.api.errors import BadRequestParams
from src.celery.task_sender import sender

from .schemas import PostSchema


class Post(MethodHandler):
    input_schema_class = PostSchema

    def handle_logic(self):
        _id = sender.send_task(
            name='SendMail',
            queue='SendMail',
            route_name='SendMail',
            kwargs=dict(
                template="demo/send_mail.html",
                to=self.payload["account"]["email"],
                subject="Xin chao",
                payload=self.payload,
            )
        )
        return {"id": str(_id)}
