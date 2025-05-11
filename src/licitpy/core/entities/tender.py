from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import HttpUrl

from licitpy.core.enums import Country
from licitpy.core.interfaces.tender import TenderAdapter


class Tender:
    def __init__(self, code: str, country: Country, adapter: TenderAdapter) -> None:

        self.code: str = code
        self.country: Country = country

        self._url: Optional[HttpUrl] = None
        self._adapter: TenderAdapter = adapter
        self._html: Optional[str] = None
        self._api_url: Optional[HttpUrl] = None
        self._data: Optional[Dict[str, Any]] = None
        self._publication_date: Optional[datetime] = None

    def api_url(self) -> HttpUrl:
        """
        Returns the Open Contracting Data Standard (OCDS) URL for the tender.
        """
        if self._api_url is not None:
            return self._api_url

        self._api_url = self._adapter.get_tender_ocds_url(self.code)
        return self._api_url

    async def aapi_url(self) -> HttpUrl:
        """
        Returns the Open Contracting Data Standard (OCDS) URL for the tender.
        """
        if self._api_url is not None:
            return self._api_url

        self._api_url = await self._adapter.aget_tender_ocds_url(self.code)
        return self._api_url

    def data(self) -> Dict[str, Any]:
        """
        Returns the OCDS JSON data of the tender.
        """
        if self._data is not None:
            return self._data

        self._data = self._adapter.get_tender_ocds_data(self.code)
        return self._data

    async def adata(self) -> Dict[str, Any]:
        """
        Asynchronously returns the OCDS JSON data of the tender.
        """
        if self._data is not None:
            return self._data

        self._data = await self._adapter.aget_tender_ocds_data(self.code)
        return self._data

    def url(self) -> HttpUrl:

        if self._url is not None:
            return self._url

        self._url = self._adapter.get_tender_url(self.code)
        return self._url

    async def aurl(self) -> HttpUrl:

        if self._url is not None:
            return self._url

        self._url = await self._adapter.aget_tender_url(self.code)
        return self._url

    def html(self) -> str:
        if self._html is not None:
            return self._html

        self._html = self._adapter.get_tender_html(self.url())
        return self._html

    async def ahtml(self) -> str:
        if self._html is not None:
            return self._html

        self._html = await self._adapter.aget_tender_html(self.url())
        return self._html

    def publication_date(self) -> datetime:
        """
        Returns the publication date of the tender.
        """
        if self._publication_date is not None:
            return self._publication_date

        self._publication_date = self._adapter.get_ocds_publication_date(self.data())

        return self._publication_date

    async def apublication_date(self) -> datetime:
        """
        Asynchronously returns the publication date of the tender.
        """
        if self._publication_date is not None:
            return self._publication_date

        self._publication_date = await self._adapter.aget_ocds_publication_date(
            await self.adata()
        )

        return self._publication_date
