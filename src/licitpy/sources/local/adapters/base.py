from pydantic import HttpUrl
from licitpy.core.interfaces.tender import TenderAdapter
from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.core.parser.parser import BaseParser


class BaseLocalTenderAdapter(TenderAdapter):
    def __init__(
        self,
        downloader: SyncDownloader,
        adownloader: AsyncDownloader,
        parser: BaseParser,
    ):
        """
        Initializes the BaseLocalTenderAdapter.

        Args:
            downloader: The synchronous HTTP downloader.
            adownloader: The asynchronous HTTP downloader.
            parser: The parser for tender data (type can be refined).
        """
        self.downloader = downloader
        self.adownloader = adownloader
        self.parser = parser

    def get_tender_html(self, url: HttpUrl) -> str:
        """
        Gets the HTML content of a tender synchronously using the provided downloader.
        """
        session = self.downloader.session
        response = session.get(str(url), timeout=30)
        response.raise_for_status()
        
        return response.text

    async def aget_tender_html(self, url: HttpUrl) -> str:
        """
        Gets the HTML content of a tender asynchronously using the provided adownloader.
        """
        session = self.adownloader.session
        async with session.get(str(url), timeout=30) as response:
            response.raise_for_status()
            
            return await response.text()
