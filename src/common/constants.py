import os
import re

import config

TMP_DIR = os.path.join(config.ROOT_PATH, 'tmp')
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

VALID_IMAGE_FORMATS = ['jpeg', 'jpg', 'png', 'webp']

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

ISO8601_DATETIME_RE = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
    r'[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
    r'(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$'
)

DATE_FORMATS = [
    dict(
        id='dd/mm/yyyy',
        js_moment='DD/MM/YYYY',
        js_element='dd/MM/yyyy',
        py='%d/%m/%Y',
        example='30/12/2020'
    ),
    dict(
        id='yyyy/mm/dd',
        js_moment='YYYY/MM/DD',
        js_element='yyyy/MM/dd',
        py='%Y/%m/%d',
        example='2020/12/30'
    ),
    dict(
        id='mm/dd/yyyy',
        js_moment='MM/DD/YYYY',
        js_element='MM/dd/yyyy',
        py='%m/%d/%Y',
        example='01/20/2020'
    )
]

TIME_FORMATS = [
    dict(
        id='hh:mm',
        js_moment='HH:mm',
        js_element='HH:mm',
        py='%H:%M',
        example='16:50'
    ),
    dict(
        id='hh:mm A',
        js_moment='hh:mm A',
        js_element='hh:mm A',
        py='%I:%M %p',
        example='07:50 PM'
    )
]

STRING_LENGTH = {
    'UUID4': 36,
    'EX_SHORT': 50,
    'SHORT': 100,
    'MEDIUM': 500,
    'LONG': 2000,
    'EX_LONG': 10000,
    'LARGE': 30000,
    'EX_LARGE': 200000
}

PAGINATION = {
    'page': 1,
    'per_page': 20
}

PHONE_REGEX = r'^(\+8[0-9]{9,12})$|^(0[0-9]{6,15})$'
LINK_REGEX = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'


DEFAULT_USER_STATUS = 'active'
DEFAULT_LANGUAGE = 'en-US'

HTTP_METHODS = [
    'GET',
    'PUT',
    'PATCH',
    'POST',
    'DELETE'
]


LANGUAGES = [
    ('en-US', 'English'),
    ('fr-FR', 'French'),
    ('zh-CN', 'Chinese (Simplified)'),
    ('ar-SA', 'Arabic'),
    ('zh-TW', 'Chinese (Traditional)'),
    ('hr-HR', 'Croatian'),
    ('vi-VN', 'Vietnamese'),
    ('cs-CZ', 'Czech'),
    ('da-DK', 'Danish'),
    ('nl-NL', 'Dutch'),
    ('fi-FI', 'Finnish'),
    ('fr-CA', 'French (Canada)'),
    ('de-DE', 'German'),
    ('el-GR', 'Greek'),
    ('hu-HU', 'Hungarian'),
    ('is-IS', 'Icelandic'),
    ('id-ID', 'Indonesian'),
    ('it-IT', 'Italian'),
    ('ja-JP', 'Japanese'),
    ('ko-KR', 'Korean'),
    ('lt-LT', 'Lithuanian'),
    ('ms-MY', 'Malay'),
    ('nb-NO', 'Norwegian'),
    ('pl-PL', 'Polish'),
    ('pt-BR', 'Portuguese (Brazil)'),
    ('pt-PT', 'Portuguese (Portugal)'),
    ('ru-RU', 'Russian'),
    ('sk-SK', 'Slovak'),
    ('es-MX', 'Spanish (Mexico)'),
    ('es-ES', 'Spanish (Spain)'),
    ('sv-SE', 'Swedish'),
    ('th-TH', 'Thai'),
    ('tr-TR', 'Turkish'),
    ('uk-UA', 'Ukrainian'),
]
