import aioinject

from src.core.di.di import Providers
from src.lib.paginator import PagePaginator

PROVIDERS: Providers = [aioinject.Scoped(PagePaginator)]
