from pydantic import HttpUrl

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.sources.local.adapters.base import BaseLocalTenderAdapter
from licitpy.sources.local.adapters.eu.parser import EuropeTenderParser

# - Fair Usage: https://ted.europa.eu/en/news/fair-usage-policy-on-ted


class EuropeTenderAdapter(BaseLocalTenderAdapter):
    """Adapter for fetching tender data from European Union's TED (Tenders Electronic Daily)."""

    def __init__(
        self,
        downloader: SyncDownloader,
        adownloader: AsyncDownloader,
        parser: EuropeTenderParser,
    ):
        """
        Initializes the EuropeTenderAdapter.

        Args:
            downloader: The synchronous HTTP downloader.
            adownloader: The asynchronous HTTP downloader.
            parser: The parser for TED tender data.
        """

        # Initialize the base class with the provided
        # downloader, adownloader, and parser.
        super().__init__(downloader, adownloader, parser)

    def _build_tender_url(self, code: str) -> HttpUrl:
        """
        Builds the direct HTML download URL for a tender, used for parsing.
        This is preferred over the public-facing URL (e.g., https://ted.europa.eu/en/notice/-/detail/<code>).
        A _build_public_tender_url method may be added in the future.

        Args:
            code: The tender identification code.
        Returns:
            The HttpUrl for the downloadable tender HTML.
        """
        url = f"https://ted.europa.eu/en/notice/{code}/html"
        return HttpUrl(url)

    def get_tender_url(self, code: str) -> HttpUrl:
        """
        Gets the URL for a specific tender synchronously.

        Args:
            code: The tender identification code.

        Returns:
            The HttpUrl for the tender.
        """
        return self._build_tender_url(code)

    async def aget_tender_url(self, code: str) -> HttpUrl:
        """
        Gets the URL for a specific tender asynchronously.

        Args:
            code: The tender identification code.

        Returns:
            The HttpUrl for the tender.
        """
        return self._build_tender_url(code)
