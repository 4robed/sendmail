from src.bases.schema import (BaseSchema, IdField, StringField,
                              STRING_LENGTH_VALIDATORS, fields)


class PostSchema(BaseSchema):
    account = StringField(required=True,
                          validate=STRING_LENGTH_VALIDATORS['LONG'])


