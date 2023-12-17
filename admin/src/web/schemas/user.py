from marshmallow import Schema
from marshmallow import fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    lastname = fields.Str()
    # confirmed = fields.Bool()
    # active = fields.Bool()
    username = fields.Str()
    email = fields.Email()
    inserted_at = fields.DateTime()
    updated_at = fields.DateTime()

users_schema = UserSchema(many=True)
user_schema = UserSchema()

