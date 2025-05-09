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

    # @abstractmethod
    # def get_tender_html(self, tender: Tender) -> str:
    #     """
    #     Get the HTML content for a specific tender using synchronous HTTP.

    #     Args:
    #         tender: The tender entity to get HTML for

    #     Returns:
    #         str: The HTML content
    #     """
    #     pass

    # @abstractmethod
    # async def get_tender_html_async(
    #     self, tender: Tender, session: ClientSession
    # ) -> str:
    #     """
    #     Get the HTML content for a specific tender using asynchronous HTTP.

    #     Args:
    #         tender: The tender entity to get HTML for
    #         session: The shared HTTP session to use

    #     Returns:
    #         str: The HTML content
    #     """
    #     pass
