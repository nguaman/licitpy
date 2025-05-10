from pydantic import HttpUrl

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.sources.local.adapters.base import BaseLocalTenderAdapter
from licitpy.sources.local.adapters.cl.parser import ChileTenderParser
from licitpy.sources.local.adapters.cl.utils.url import (
    _build_lookup_tender_url,
    _build_url_from_redirect_header,
)


class ChileTenderAdapter(BaseLocalTenderAdapter):
    """Provider for Chilean tenders from MercadoPublico."""

    _BASE_URL = (
        "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"
    )

    def __init__(
        self,
        downloader: SyncDownloader,
        adownloader: AsyncDownloader,
        parser: ChileTenderParser,
    ):
        """
        Initializes the EuropeTenderAdapter.

        Args:
            downloader: The synchronous HTTP downloader.
            adownloader: The asynchronous HTTP downloader.
            parser: The parser for Chilean tender data.
        """
        # Initialize the base class with the provided
        # downloader, adownloader, and parser.
        super().__init__(downloader, adownloader, parser)

    def get_tender_url(self, code: str) -> HttpUrl:
        """Get the tender URL for a given code."""
        lookup_url = _build_lookup_tender_url(self._BASE_URL, code)

        session = self.downloader.session
        response = session.head(lookup_url, timeout=30, allow_redirects=False)

        return _build_url_from_redirect_header(
            self._BASE_URL, response.headers["Location"]
        )

    async def aget_tender_url(self, code: str) -> HttpUrl:
        """Asynchronously get the tender URL for a given code."""
        lookup_url = _build_lookup_tender_url(self._BASE_URL, code)

        session = self.adownloader.session
        response = await session.head(lookup_url, timeout=30, allow_redirects=False)

        return _build_url_from_redirect_header(
            self._BASE_URL, response.headers["Location"]
        )
