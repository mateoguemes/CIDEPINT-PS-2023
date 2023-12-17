from marshmallow import Schema
from marshmallow import fields

class ServiceSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    laboratory = fields.Str()
    keywords = fields.Str()
    id = fields.Int()
    
services_schema = ServiceSchema(many=True)
service_schema = ServiceSchema()


