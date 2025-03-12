import aioinject

from typing import TypeAlias, Iterable, Any


Providers: TypeAlias = Iterable[aioinject.Provider[Any]]

INJECTED: Any = object()
"""Hack for Liskov principe"""
