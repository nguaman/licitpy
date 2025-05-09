from pydantic import HttpUrl

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.core.interfaces.tender import TenderAdapter
from licitpy.sources.local.adapters.cl.parser import ChileTenderParser


class ChileTenderAdapter(TenderAdapter):
    """Provider for Chilean tenders from MercadoPublico."""

    def __init__(
        self,
        downloader: SyncDownloader,
        adownloader: AsyncDownloader,
        parser: ChileTenderParser,
    ):

        self.downloader = downloader
        self.adownloader = adownloader
        self.parser = parser

    def get_tender_url(self, code: str) -> HttpUrl:
        """Get MercadoPublico URL for a tender."""
        base_url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"

        session = self.downloader.session

        response = session.head(
            f"{base_url}?idlicitacion={code}", timeout=30, allow_redirects=False
        )

        query = response.headers["Location"].split("qs=")[1].strip()

        return HttpUrl(f"{base_url}?qs={query}")

    async def aget_tender_url(self, code: str) -> HttpUrl:
        """Asynchronous version using aiohttp. Assumes session is managed externally (via async with Licitpy or licitpy.initialize())."""
        base_url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"

        session = self.adownloader.session

        response = await session.head(
            f"{base_url}?idlicitacion={code}", timeout=30, allow_redirects=False
        )

        query = response.headers["Location"].split("qs=")[1].strip()

        return HttpUrl(f"{base_url}?qs={query}")
