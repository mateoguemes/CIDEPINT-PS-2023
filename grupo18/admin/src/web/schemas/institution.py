from marshmallow import Schema
from marshmallow import fields

class InstitutionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    information = fields.Str()
    address = fields.Str()
    location = fields.Str()
    website = fields.Str()
    opening_hours = fields.Str()
    contact = fields.Str()
    enabled = fields.Bool()
    inserted_at = fields.DateTime()
    updated_at = fields.DateTime()

institutions_schema = InstitutionSchema(many=True)
institution_schema = InstitutionSchema()

