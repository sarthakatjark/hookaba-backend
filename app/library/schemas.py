from marshmallow import Schema, fields

class LibraryItemSchema(Schema):
    url = fields.Str(required=True)
    user_id = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    type = fields.Str(required=True)
    category = fields.Str(required=True) 