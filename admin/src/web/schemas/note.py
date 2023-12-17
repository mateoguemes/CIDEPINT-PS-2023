from marshmallow import Schema
from marshmallow import fields

class NoteSchema(Schema):
    requirement_id = fields.Int(dump_only=True)
    text = fields.Str()
    inserted_at = fields.DateTime()
    from_laboratory = fields.Boolean()

notes_schema = NoteSchema(many=True)
note_schema = NoteSchema()

