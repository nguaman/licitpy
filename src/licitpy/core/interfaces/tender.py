from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, AsyncIterator, Dict, Iterator

from pydantic import HttpUrl


class TenderAdapter(ABC):
    """
    Abstract base class for tender data providers.
    Concrete implementations will be created for each country.
    """

    @abstractmethod
    def get_tender_url(self, code: str) -> HttpUrl:
        pass

    @abstractmethod
    async def aget_tender_url(self, code: str) -> HttpUrl:
        pass

    @abstractmethod
    def get_tender_html(self, url: HttpUrl) -> str:
        pass

    @abstractmethod
    async def aget_tender_html(self, url: HttpUrl) -> str:
        pass

    @abstractmethod
    def get_tenders_from_date(self, year: int, month: int, day: int) -> Iterator[str]:
        pass

    @abstractmethod
    def aget_tenders_from_date(
        self, year: int, month: int, day: int
    ) -> AsyncIterator[str]:
        pass

    @abstractmethod
    def get_tender_ocds_url(self, code: str) -> HttpUrl:
        pass

    @abstractmethod
    async def aget_tender_ocds_url(self, code: str) -> HttpUrl:
        pass

    @abstractmethod
    def get_tender_ocds_data(self, code: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def aget_tender_ocds_data(self, code: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_ocds_publication_date(self, data: Dict[str, Any]) -> datetime:
        pass

    @abstractmethod
    async def aget_ocds_publication_date(self, data: Dict[str, Any]) -> datetime:
        pass
