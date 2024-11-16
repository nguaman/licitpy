from datetime import datetime
from typing import Optional

from pydantic import HttpUrl

from licitpy.downloader.tender import TenderDownloader
from licitpy.parsers.tender import TenderParser
from licitpy.types import Status, Tier
from licitpy.utils.decorators import singleton


@singleton
class TenderServices:

    def __init__(
        self,
        downloader: Optional[TenderDownloader] = None,
        parser: Optional[TenderParser] = None,
    ):

        self.downloader: TenderDownloader = downloader or TenderDownloader()
        self.parser: TenderParser = parser or TenderParser()

    def get_status(self, data: dict) -> Status:
        return self.parser.get_tender_status_from_tender_ocds_data(data)

    def get_ocds_data(self, code: str) -> dict:
        return self.downloader.get_tender_ocds_data(code)

    def get_url(self, code: str) -> HttpUrl:
        return self.downloader.get_tender_url_from_code(code)

    def get_name(self, data: dict) -> str:
        return self.parser.get_tender_title_from_tender_ocds_data(data)

    def get_title(self, data: dict) -> str:
        return self.parser.get_tender_title_from_tender_ocds_data(data)

    def get_opening_date(self, data: dict) -> datetime:
        return self.parser.get_tender_opening_date_from_tender_ocds_data(data)

    def get_html(self, url: HttpUrl) -> str:
        return self.downloader.get_html_from_url(url)

    def get_tender_codes(self, year: int, month: int):
        return self.downloader.get_tender_codes(year, month)

    def get_tier(self, code: str) -> Tier:
        return self.parser.get_tender_tier(code)
