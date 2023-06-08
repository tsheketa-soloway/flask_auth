from app import ma
from marshmallow import pre_load
from models import User
from werkzeug.security import generate_password_hash

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances
        exclude = ('password_hash',)

    password = ma.String(required=True, load_only=True)

    @pre_load
    def hash_password(self, in_data, **kwargs):
        if "password" in in_data:
            in_data["password_hash"] = generate_password_hash(in_data["password"])
            del in_data["password"]
        return in_data
