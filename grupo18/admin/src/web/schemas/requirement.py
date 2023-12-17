from marshmallow import Schema
from marshmallow import fields

class RequirementSchema(Schema):
    creation_date = fields.DateTime()
    close_date = fields.DateTime()
    service_name = fields.Str()
    description = fields.Str()
    current_status = fields.Str()
    requirement_id = fields.Int()
    client_description = fields.Str()
    observation = fields.Str()
    service_id = fields.Int()
    
requirements_schema = RequirementSchema(many=True)
requirement_schema = RequirementSchema()

class StatusQuantitySchema(Schema):
    status = fields.Str()
    quantity = fields.Int()

status_quantities_schema = StatusQuantitySchema(many=True)
status_quantity_schema = StatusQuantitySchema()