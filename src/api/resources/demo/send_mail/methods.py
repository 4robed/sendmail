from src.bases.api.method_handler import MethodHandler
from src.bases.api.errors import BadRequestParams
from src.celery.task_sender import sender
from src.common.constants import LANGUAGES_FOLDER, LANGUAGES_SUBJECT

from .schemas import PostSchema


class Post(MethodHandler):
    input_schema_class = PostSchema

    def handle_logic(self):
        folder = LANGUAGES_FOLDER[self.request.headers["Accept-Language"]]
        subject = LANGUAGES_SUBJECT[self.request.headers["Accept-Language"]]
        _id = sender.send_task(
            name='SendMail',
            queue='SendMail',
            route_name='SendMail',
            kwargs=dict(
                template=f"{folder}/demo/send_mail.html",
                to=self.payload["account"]["email"],
                subject=subject,
                payload=self.payload,
            )
        )

        return {"id": str(_id)}
