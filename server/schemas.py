from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)

class JournalEntrySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(validate=validate.Length(max=50))
    mood_score = fields.Int(validate=validate.Range(min=1, max=10))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)

user_schema = UserSchema()
entry_schema = JournalEntrySchema()
entries_schema = JournalEntrySchema(many=True)