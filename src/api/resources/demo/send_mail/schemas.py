from src.bases.schema import (BaseSchema, IdField, StringField,
                              STRING_LENGTH_VALIDATORS, EmailField,
                              NestedField, LinkField)


class AccountSchema(BaseSchema):
    email = EmailField(required=True)
    name = StringField(required=True)


class InfoSchema(BaseSchema):
    description = StringField(required=True)


class PostSchema(BaseSchema):
    account = NestedField(AccountSchema, required=True)
    info = NestedField(InfoSchema, required=True)
