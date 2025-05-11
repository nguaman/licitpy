import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from typing import Any, AsyncIterator, Dict, Iterator
from zoneinfo import ZoneInfo

from pydantic import HttpUrl
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.core.exceptions import InvalidTenderDataException
from licitpy.sources.local.adapters.base import BaseLocalTenderAdapter
from licitpy.sources.local.adapters.cl.parser import ChileTenderParser
from licitpy.sources.local.adapters.cl.services.tender_aggregator import (
    ChileanTenderAggregatorService,
)
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
        data: ChileanTenderAggregatorService,
    ):
        """
        Initializes the ChileTenderAdapter.

        Args:
            downloader: The synchronous HTTP downloader.
            adownloader: The asynchronous HTTP downloader.
            parser: The parser for Chilean tender data.
            data: The service for aggregating tender data.
        """

        # Initialize the base class with the provided
        # downloader, adownloader.
        super().__init__(downloader, adownloader)

        self.data = data
        self.parser = parser

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

    def get_tender_ocds_url(self, code: str) -> HttpUrl:
        """
        Get the OCDS URL for a given tender code.

        Args:
            code: The unique identification code of the tender.

        Returns:
            The OCDS URL for the specified tender code.
        """
        return HttpUrl(f"https://apis.mercadopublico.cl/OCDS/data/record/{code}")

    async def aget_tender_ocds_url(self, code: str) -> HttpUrl:
        """
        Asynchronously get the OCDS URL for a given tender code.

        Args:
            code: The unique identification code of the tender.

        Returns:
            The OCDS URL for the specified tender code.
        """
        return HttpUrl(f"https://apis.mercadopublico.cl/OCDS/data/record/{code}")

    def get_tender_ocds_data(self, code: str) -> Dict[str, Any]:
        """
        Get the OCDS data for a given tender code.

        Args:
            code: The unique identification code of the tender.

        Returns:
            The OCDS data for the specified tender code.
        """
        url = self.get_tender_ocds_url(code)

        session = self.downloader.session
        response = session.get(str(url), timeout=30)
        response.raise_for_status()

        data = response.json()

        # Validate that the 'records' field exists
        if "records" not in data or not data["records"]:
            raise InvalidTenderDataException(
                f"Invalid OCDS data for tender {code}: 'records' field missing"
            )

        return data

    @retry(
        retry=retry_if_exception_type((InvalidTenderDataException, ConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def aget_tender_ocds_data(self, code: str) -> Dict[str, Any]:
        """
        Asynchronously get the OCDS data for a given tender code.

        Args:
            code: The unique identification code of the tender.

        Returns:
            The OCDS data for the specified tender code.
        """
        url = self.get_tender_ocds_url(code)

        session = self.adownloader.session

        async with session.get(str(url), timeout=30) as response:
            response.raise_for_status()
            data = await response.json()

            # Validate that the 'records' field exists
            if "records" not in data or not data["records"]:
                raise InvalidTenderDataException(
                    f"Invalid OCDS data for tender {code}: 'records' field missing"
                )

            return data

    def get_ocds_publication_date(self, data: Dict[str, Any]) -> datetime:
        """
        Extract the publication date from tender OCDS data.

        Args:
            data: The OCDS data dictionary containing tender information.

        Returns:
            The publication date of the tender with Santiago timezone.
        """
        dates = data["records"][0]["compiledRelease"]["tender"]["tenderPeriod"]

        # Parse the start date from the JSON data
        start_date: datetime = datetime.strptime(
            dates["startDate"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=ZoneInfo("America/Santiago"))

        return start_date

    async def aget_ocds_publication_date(self, data: Dict[str, Any]) -> datetime:
        """
        Asynchronously extract the publication date from tender OCDS data.

        Args:
            data: The OCDS data dictionary containing tender information.

        Returns:
            The publication date of the tender with Santiago timezone.
        """
        dates = data["records"][0]["compiledRelease"]["tender"]["tenderPeriod"]

        # Parse the start date from the JSON data
        start_date: datetime = datetime.strptime(
            dates["startDate"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=ZoneInfo("America/Santiago"))

        return start_date

    def _is_tender_published_on_date(self, code: str, when: date | datetime) -> bool:

        data = self.get_tender_ocds_data(code)
        dates = data["records"][0]["compiledRelease"]["tender"]["tenderPeriod"]

        # Parse the start date from the JSON data
        start_date: datetime = datetime.strptime(
            dates["startDate"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=ZoneInfo("America/Santiago"))

        return (
            start_date.year == when.year
            and start_date.month == when.month
            and start_date.day == when.day
        )

    async def _ais_tender_published_on_date(
        self, code: str, when: date | datetime
    ) -> bool:

        data = await self.aget_tender_ocds_data(code)

        dates = data["records"][0]["compiledRelease"]["tender"]["tenderPeriod"]

        # Parse the start date from the JSON data
        start_date: datetime = datetime.strptime(
            dates["startDate"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=ZoneInfo("America/Santiago"))

        return (
            start_date.year == when.year
            and start_date.month == when.month
            and start_date.day == when.day
        )

    def get_tenders_from_date(self, year: int, month: int, day: int) -> Iterator[str]:

        codes_from_csv = self.data.get_tenders_codes_from_csv(year, month)
        codes_from_api = self.data.get_tenders_codes_from_api(year, month)

        # Combine the codes from both sources, removing duplicates
        codes = list(set(codes_from_api) | set(codes_from_csv))

        # Sort the codes to ensure consistent order
        codes.sort()

        # Use ThreadPoolExecutor to fetch data concurrently
        with ThreadPoolExecutor(max_workers=32) as executor:

            future_to_code = {
                executor.submit(
                    self._is_tender_published_on_date, code, date(year, month, day)
                ): code
                for code in codes
            }

            # Process results as they complete
            for future in as_completed(future_to_code):

                code = future_to_code[future]
                result = future.result()

                # If the tender matches the date criteria, yield it
                if result:
                    yield code

    async def aget_tenders_from_date(
        self, year: int, month: int, day: int
    ) -> AsyncIterator[str]:

        # Execute both async operations concurrently
        codes_from_csv, codes_from_api = await asyncio.gather(
            self.data.aget_tenders_codes_from_csv(year, month),
            self.data.aget_tenders_codes_from_api(year, month),
        )

        # Combine the codes from both sources, removing duplicates
        codes = list(set(codes_from_api) | set(codes_from_csv))

        # Sort the codes to ensure consistent order
        codes.sort()

        # Use asyncio.Semaphore to limit the number of concurrent tasks
        semaphore = asyncio.Semaphore(32)

        async def check_code(code: str) -> tuple[str, bool]:
            async with semaphore:
                return code, await self._ais_tender_published_on_date(
                    code, date(year, month, day)
                )

        tasks = [asyncio.create_task(check_code(code)) for code in codes]

        try:
            for task in asyncio.as_completed(tasks):
                code, is_published = await task

                if is_published:
                    yield code
        finally:

            # Check for any pending tasks
            pending_tasks = [task for task in tasks if not task.done()]

            # Cancel any pending tasks
            for task in pending_tasks:
                if not task.done():
                    task.cancel()

            # Wait for all pending tasks to finish
            if pending_tasks:
                await asyncio.wait(pending_tasks, timeout=1)
