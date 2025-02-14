import functools
import aioinject
import importlib
import pkgutil

from collections.abc import Sequence, Iterable
from types import ModuleType

from database.dependencies import create_session
from settings import get_settings, PostgresqlSettings
from pydantic_settings import BaseSettings
from . import _modules

from aioinject import Provider

SETTINGS = (PostgresqlSettings,)


def autodiscover_providers(
    module: ModuleType,
    attr_name: str,
    *,
    raise_error: bool = True,
) -> Sequence[Provider[object]]:
    result: list[Provider[object]] = []
    for submodule_info in pkgutil.walk_packages(
        module.__path__, f"{module.__name__}."
    ):
        submodule = importlib.import_module(submodule_info.name)
        module_providers = getattr(submodule, attr_name, None)
        if module_providers is None:
            if raise_error:
                msg = f"Module {submodule_info.name} does not have {attr_name} attribute"  # noqa: E501
                raise ValueError(msg)
            continue
        result.extend(module_providers)
    return result


def _register_settings(
    container: aioinject.Container,
    *,
    settings_classes: Iterable[type[BaseSettings]],
) -> None:
    for settings_cls in settings_classes:
        factory = functools.partial(get_settings, settings_cls)
        container.register(aioinject.Singleton(factory, type_=settings_cls))


@functools.lru_cache
def create_container() -> aioinject.Container:
    container = aioinject.Container()
    container.register(aioinject.Scoped(create_session))

    for provider in autodiscover_providers(_modules, attr_name="PROVIDERS"):
        container.register(provider)

    _register_settings(container, settings_classes=SETTINGS)

    return container
