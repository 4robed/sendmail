from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from jinja2 import Environment, FileSystemLoader

from src.bases.error import ClientError
from src.common.utils import log
from config import ROOT_PATH


class Mail(object):
    def __init__(self, app_name, username, password, port, host, support, website):
        self.app_name = app_name
        self.username = username
        self.password = password
        self.port = port
        self.host = host
        self.support = support
        self.website = website

    def render_template(self, template, payload):
        env = Environment(loader=FileSystemLoader(
            f'{ROOT_PATH}/src/sendmail/templates/'
        ))
        try:
            template = env.get_template(template)
        except:
            raise ClientError("TemplateNotFound")

        return template.render(data=payload)

    def send_mail(self,
                  template,
                  to,
                  subject,
                  payload,
                  dirs=None):
        log.info(f'SEND: to={to}')
        sender = self.username
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = f"{self.app_name} <{sender}>"
        message['To'] = to
        data = dict(
            support=self.support,
            website=self.website,
            payload=payload
        )
        message.attach(MIMEText(
            self.render_template(template, data), "html")
        )

        if dirs:
            for _dir in dirs:
                try:
                    file_name = _dir.split("/")[-1]
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(_dir, "rb").read())

                    encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', filename=file_name)
                    message.attach(part)
                except Exception as e:
                    print(f'Attach file failed: e={e}')

        server = SMTP(self.host, self.port)
        server.starttls()
        server.login(sender, self.password)
        server.sendmail(sender, to, message.as_string())

        server.quit()
