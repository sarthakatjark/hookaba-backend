from marshmallow import Schema, fields

class RequestOTPSchema(Schema):
    phone = fields.String(required=True)
    platform = fields.String(required=False)

class VerifyOTPSchema(Schema):
    phone = fields.Str(required=True)
    otp = fields.Str(required=True) 