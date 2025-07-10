from marshmallow import Schema, fields

class LibraryItemSchema(Schema):
    url = fields.Str(required=True)
    user_id = fields.Str(required=True)
    created_at = fields.DateTime(required=True) 