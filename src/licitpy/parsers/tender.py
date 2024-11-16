from datetime import datetime
from zoneinfo import ZoneInfo

from licitpy.parsers.base import BaseParser
from licitpy.types import Status, Tier


class TenderParser(BaseParser):

    def get_tender_opening_date_from_tender_ocds_data(self, data: dict) -> datetime:

        # The date comes as if it were UTC, but it is actually America/Santiago
        # - 2024-11-06T11:40:34Z -> 2024-11-06 11:40:34-03:00

        tender = data["records"][0]["compiledRelease"]["tender"]
        start_date = tender["tenderPeriod"]["startDate"]

        return datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_tender_status_from_tender_ocds_data(self, data: dict) -> Status:
        tender = data["records"][0]["compiledRelease"]["tender"]
        return Status(tender["status"])

    def get_tender_title_from_tender_ocds_data(self, data: dict) -> str:
        tender = data["records"][0]["compiledRelease"]["tender"]
        return tender["title"]

    def get_tender_tier(self, code: str) -> Tier:
        return Tier(code.split("-")[-1:][0][:2])
