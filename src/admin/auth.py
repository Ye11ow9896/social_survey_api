from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.core.di.di import INJECTED
from src.database.models.user_admin import UserAdmin
from src.core.domain.auth.repository import AuthRepository
from src.core.domain.auth.service import AuthenticationService
from src.settings import AuthSettings
from aioinject import Injected
from aioinject.ext.litestar import inject


class AdminAuth(AuthenticationBackend):
    @inject
    async def login(
        self,
        request: Request,
        auth_repository: Injected[AuthRepository] = INJECTED,
        settings: Injected[AuthSettings] = INJECTED,
        service: Injected[AuthenticationService] = INJECTED,
    ) -> UserAdmin | None:
        form = await request.form()
        username, password = form["username"], form["password"]
        request.session.update({"token": "..."})
        auth_data = await auth_repository.get_useradmin(username=username)
        if auth_data is not None:
            hashed_password = service.get_hashed_password(password=password)
            if auth_data.hashed_password == hashed_password:
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True
