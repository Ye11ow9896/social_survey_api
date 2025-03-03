from sqladmin_litestar_plugin import SQLAdminPlugin

from admin.auth import AdminAuth
from database.engine import engine
from src.admin.views import _VIEWS

def get_admin_plugin() -> SQLAdminPlugin:
    return SQLAdminPlugin(
        views=_VIEWS,
        engine=engine,
        authentication_backend=AdminAuth(secret_key="...")
    )