from src.bases.api.method_handler import MethodHandler
from src.bases.api.errors import BadRequestParams
from src.celery.task_sender import sender
from .schemas import PostSchema
from src.common.constants import LANGUAGE_FOLDERS


subjects = {'vi': 'Xin chao', 'en': 'Hi'}


class Post(MethodHandler):
    input_schema_class = PostSchema

    def handle_logic(self):
        language_code = self.payload['language_code']
        if language_code not in LANGUAGE_FOLDERS:
            raise BadRequestParams('Language not supported')
        _id = sender.send_task(
            name='SendMail',
            queue='SendMail',
            route_name='SendMail',
            kwargs=dict(
                template=f'{LANGUAGE_FOLDERS[language_code]}/demo/send_mail.html',
                to=self.payload['account']['email'],
                subject=subjects[language_code],
                payload=self.payload,
            )
        )

        return {'id': str(_id)}
