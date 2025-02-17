from core.dto import BaseDTO


class LoginCredentialsDTO(BaseDTO):
    service_name: str
    password: str
