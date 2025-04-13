from types import SimpleNamespace
from uuid import UUID


class RoleIdConstant(SimpleNamespace):
    ADMIN = UUID("019513e1-a3a0-7e71-968e-8a2351dbccf1")
    RESPONDENT = UUID("019513e1-baf0-7872-9158-154709ef272e")
    OWNER = UUID("60735458-d191-4a22-8759-9077705609ea")
