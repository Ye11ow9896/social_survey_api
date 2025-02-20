import aioinject

from core.di.di import Providers
from lib.paginator import PagePaginator

PROVIDERS: Providers = [
    aioinject.Scoped(PagePaginator)
]