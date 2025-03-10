import uuid
from src.adapters.api.schema import BaseSchema


class LoginCredentialsSchema(BaseSchema):
    login: str
    password: str

class UserAdminSchema(BaseSchema):
    username: uuid.UUID
    hashed_password: str