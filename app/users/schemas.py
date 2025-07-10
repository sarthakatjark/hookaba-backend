from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.Str(required=True)
    number = fields.Str(required=True) 