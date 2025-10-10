from marshmallow import fields, validate
from .extensions import ma
from .models import BlacklistModel

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    email = fields.Email(required=True)
    app_uuid = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta:
        model = BlacklistModel
        fields = ("id", "email", "app_uuid", "blocked_reason", "created_at")
        load_instance = True
