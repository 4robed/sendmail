import re
from marshmallow import fields, ValidationError
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.wsgi import LimitedStream

from src.common.constants import (STRING_LENGTH, PHONE_REGEX,
                                  DATE_FORMATS, LINK_REGEX)


class IntegerField(fields.Integer):
    pass


class FloatField(fields.Float):
    pass


class BooleanField(fields.Boolean):
    pass


class NestedField(fields.Nested):
    pass


class StringField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) and value:
            value = value.strip()

        return super()._deserialize(value, attr, data, **kwargs)


class EmailField(fields.Email):
    pass


class LinkField(fields.String):

    def _validate(self, value):
        super()._validate(value)
        if not re.compile(LINK_REGEX).match(value):
            raise ValidationError('Invalid link.')


class RawField(fields.Raw):
    pass


class IdField(StringField):
    def _validate(self, value):
        super()._validate(value)
        if isinstance(value, ObjectId):
            return value
        try:
            ObjectId(value)
        except Exception as error:
            raise ValidationError('Invalid object id %s' % error.args)


class PhoneField(StringField):
    def _validate(self, value):
        super()._validate(value)
        if not re.compile(PHONE_REGEX).match(value):
            raise ValidationError('Invalid phone.')


class DatetimeField(fields.DateTime):
    def _validate(self, value):
        if not isinstance(value, datetime):
            if isinstance(value, float) or isinstance(value, int):
                try:
                    value = datetime.fromtimestamp(value)
                except Exception:
                    raise ValidationError('Invalid datetime!')
        return super()._validate(value)

    def _deserialize(self, value, attr=None, data=None, **kwargs):
        if isinstance(value, (str, int)):
            try:
                value = float(value)
            except ValueError:
                pass

        if isinstance(value, float):
            value = datetime.fromtimestamp(value)
        return super()._deserialize(value, attr, data, **kwargs)


class FileField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, FileStorage):
            raise ValidationError('Invalid file.')


class StreamField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, LimitedStream):
            raise ValidationError('Invalid stream.')


class ListField(fields.List):
    def _validate(self, value):
        if isinstance(value, str):
            if not value:
                value = []
            else:
                value = value.split(',')

        return super()._validate(value)

    def _deserialize(self, value, attr=None, data=None, **kwargs):
        if isinstance(value, str):
            if not value:
                value = []
            else:
                value = value.split(',')
        return super()._deserialize(value, attr, data, **kwargs)


class RangeField(ListField):
    def _validate(self, value):
        super()._validate(value)
        if len(value) != 2:
            raise ValidationError('Must contain only 2 values')


class TimeField(StringField):
    def _validate(self, value):
        super()._validate(value)
        if len(value) > 5:
            raise ValidationError('Invalid time.')
        try:
            hour, minute = value.split(':')
            hour = int(hour)
            minute = int(minute)
        except ValueError:
            raise ValidationError('Invalid time.')

        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValidationError('Invalid time.')
