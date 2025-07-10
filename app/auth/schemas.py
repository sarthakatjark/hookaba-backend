from marshmallow import Schema, fields

class RequestOTPSchema(Schema):
    phone = fields.Str(required=True)

class VerifyOTPSchema(Schema):
    phone = fields.Str(required=True)
    otp = fields.Str(required=True) 