from sqladmin_litestar_plugin import SQLAdminPlugin

from src.adapters.admin.auth import AdminAuth
from src.database.engine import engine
from src.adapters.admin.views import _VIEWS


def get_admin_plugin() -> SQLAdminPlugin:
    return SQLAdminPlugin(
        views=_VIEWS,
        engine=engine,
        authentication_backend=AdminAuth(secret_key="..."),
    )
