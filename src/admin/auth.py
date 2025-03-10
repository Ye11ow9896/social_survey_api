import hashlib
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from database.models.user_admin import UserAdmin
from src.core.domain.auth.repository import AuthRepository
from src.core.domain.auth.service import AuthenticationService
from src.adapters.api.auth.schema import UserAdminSchema
from src.settings import AuthSettings



class AdminAuth(AuthenticationBackend):
    def __init__(
        self,
        auth_repository: AuthRepository,
        settings: AuthSettings,
    ) -> None:
        self._auth_repository = auth_repository
        self._settings = settings

    async def login(
            self, request: Request,
            # auth_service: AuthenticationService,
            ) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]  # noqa: F841 Будет использоваться когда будет таблица админа
        request.session.update({"token": "..."})
        auth_data = self._auth_repository.get_useradmin_by_username(username=username)
        if isinstance(auth_data, UserAdmin):
            hashed_password = self._get_hashed_password(password=password)
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

    # Либо взять напрямую из AuthenticationService, либо вынести куда-то
    def _get_hashed_password(self, password: str) -> str:
        convert_password = str.encode(
            password + self._settings.salt, encoding="utf-8"
        )
        return hashlib.md5(convert_password).hexdigest()