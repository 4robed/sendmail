import yaml
import os

ROOT_PATH = os.path.dirname(__file__)

CONFIG_FILE_PATH = os.path.join(ROOT_PATH, 'env.yaml')

if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as r_file:
        data = yaml.safe_load(r_file)
else:
    data = dict()

ENVIRONMENT = data.get('ENVIRONMENT', 'local')

SECRET_KEY = data.get('SECRET_KEY', 'secret_key')

VERSION = data.get('VERSION', 'v1')

LOG_FILE = data.get('LOG_FILE', 'tmp/output.log')

REDIS = data.get('REDIS', dict(
    password='813417',
    host='localhost',
    port=6379,
))

SENTRY_DNS = data.get('SENTRY_DNS', 'http://localhost:5000')

SMTP = data.get('SMTP', dict(
    app_name='',
    username='',
    password='',
    port='',
    host='',
    support='',
    website=''
))


class CeleryConfig(object):
    env = ENVIRONMENT

    broker_url = 'redis://:{password}@{host}:{port}/{db}'.format(
        password=REDIS['password'],
        host=REDIS['host'],
        port=REDIS['port'],
        db=0,
    )

    sentry_dns = SENTRY_DNS


class ApiConfig(object):
    APP_NAME = 'Sendmail service'

    ENV = ENVIRONMENT

    SECRET_KEY = SECRET_KEY

    SENTRY_DNS = SENTRY_DNS


class SMTPConfig(object):
    app_name = SMTP['app_name']
    username = SMTP['username']
    password = SMTP['password']
    port = SMTP['port']
    host = SMTP['host']
    support = SMTP['support']
    website = SMTP['website']
