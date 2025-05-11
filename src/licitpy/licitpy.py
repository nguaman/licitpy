from contextlib import AbstractAsyncContextManager, AbstractContextManager
from datetime import timedelta
from types import TracebackType
from typing import Dict, List, Optional, Type, Union

from licitpy.core.containers.container import Container
from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country
from licitpy.core.query import TenderQuery
from licitpy.sources.api.source import API
from licitpy.sources.local.source import Local


class CountryClient:

    def __init__(self, source: Union[API, Local], country: Country) -> None:

        self.source = source
        self.country = country

    def get(self, code: str) -> Tender:
        return self.source.get_tender_by_code(code, country=self.country)

    async def aget(self, code: str) -> Tender:
        return await self.source.aget_tender_by_code(code, country=self.country)

    def get_tenders_by_codes(self, codes: List[str]) -> List[Tender]:
        return self.source.get_tenders_by_codes(codes, country=self.country)

    def search(self) -> TenderQuery:
        return TenderQuery(source=self.source, country=self.country)


class Licitpy(
    AbstractContextManager["Licitpy"], AbstractAsyncContextManager["Licitpy"]
):
    def __init__(
        self,
        api_key: str | None = None,
        use_cache: bool = True,
        expire_after: timedelta = timedelta(hours=6),
        disable_progress_bar: bool = False,
        container: Optional[Container] = None,
    ):
        self.container = container or Container()

        self.container.config.use_cache.override(use_cache)
        self.container.config.cache_expire_after.override(expire_after)
        self.container.config.disable_progress_bar.override(disable_progress_bar)

        self.source: Union[API, Local]

        if api_key:
            self.source = API(api_key=api_key)
        else:
            self.source = Local(country_providers=self.container.country_providers())

        self._country_clients: Dict[Country, CountryClient] = {}

    async def __aenter__(self) -> "Licitpy":
        """Initializes async resources when entering an async context."""
        await self.container.adownloader().open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Closes async resources when exiting an async context."""
        await self.container.adownloader().close()
        return None

    def __enter__(self) -> "Licitpy":
        """Initializes sync resources when entering a sync context."""
        self.container.downloader().open()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Closes sync resources when exiting a sync context."""
        self.container.downloader().close()
        return None

    def __getitem__(self, country: Country) -> CountryClient:
        """Get the client for a specific country."""
        if country not in self._country_clients:
            self._country_clients[country] = CountryClient(self.source, country)
        return self._country_clients[country]

    @property
    def cl(self) -> CountryClient:
        """Client for Chilean tenders."""
        if Country.CL not in self._country_clients:
            self._country_clients[Country.CL] = CountryClient(self.source, Country.CL)
        return self._country_clients[Country.CL]

    @property
    def eu(self) -> CountryClient:
        """Client for European tenders."""
        if Country.EU not in self._country_clients:
            self._country_clients[Country.EU] = CountryClient(self.source, Country.EU)
        return self._country_clients[Country.EU]
