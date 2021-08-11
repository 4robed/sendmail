from src.api.bases import BaseResource
import requests


class SendmailResource(BaseResource):
    auth_required = False
    endpoint = '/demo/send_mail'

