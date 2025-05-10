from abc import ABC, abstractmethod

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
    

