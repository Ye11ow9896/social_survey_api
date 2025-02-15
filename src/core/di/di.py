import aioinject

from typing import TypeAlias, Iterable, Any

Providers: TypeAlias = Iterable[aioinject.Provider[Any]]
