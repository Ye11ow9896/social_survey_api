from adapters.api.schema import BaseSchema


class LoginCredentialsSchema(BaseSchema):
    login: str
    password: str
