from src.common.utils import log
from src.bases.celery.task import Task, LogicHandler as BaseLogicHandler
from src.sendmail.base import Mail
from config import SMTPConfig


class LogicHandler(BaseLogicHandler):
    def run(self, template,
            to,
            subject,
            payload,
            dirs=None,
            ):
        log.info('SENDMAIL start')
        mail = Mail(
            app_name=SMTPConfig.app_name,
            username=SMTPConfig.username,
            password=SMTPConfig.password,
            port=SMTPConfig.port,
            host=SMTPConfig.host,
            support=SMTPConfig.support,
            website=SMTPConfig.website,
        )
        mail.send_mail(
            template=template,
            to=to,
            subject=subject,
            payload=payload,
            dirs=dirs,
        )
        log.info('SENDMAIL done')


class SendMailHandler(Task):
    name = 'SendMail'
    logic_handler_class = LogicHandler
