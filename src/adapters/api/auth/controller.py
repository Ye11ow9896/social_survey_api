from litestar import get
from litestar.controller import Controller

from adapters.api.auth.schema import RoleSchema
from aioinject import Injected
from aioinject.ext.fastapi import inject

from core.domain.auth.service import AuthService


class AuthController(Controller):
    path = "/auth"
    tags = ("Auth endpoints",)

    @get("/authorization", status_code=200)
    @inject
    async def test(self, service: Injected[AuthService]) -> list[RoleSchema]:
        result = await service.test()
        return RoleSchema.model_validate_list(result)
