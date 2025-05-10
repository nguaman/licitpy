from typing import Optional

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
    