from datetime import datetime
from zoneinfo import ZoneInfo

from licitpy.parsers.base import BaseParser
from licitpy.types.tender.open_contract import OpenContract, PartyRoleEnum
from licitpy.types.tender.status import StatusFromImage, StatusFromOpenContract
from licitpy.types.tender.tender import Region, Tier


class TenderParser(BaseParser):

    def get_tender_opening_date_from_tender_ocds_data(
        self, data: OpenContract
    ) -> datetime:

        # The date comes as if it were UTC, but it is actually America/Santiago
        # - 2024-11-06T11:40:34Z -> 2024-11-06 11:40:34-03:00

        tender = data.records[0].compiledRelease.tender
        start_date = tender.tenderPeriod.startDate

        return datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_closing_date_from_tender_ocds_data(self, data: OpenContract) -> datetime:
        tender = data.records[0].compiledRelease.tender
        end_date = tender.tenderPeriod.endDate

        return datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_tender_status_from_tender_ocds_data(
        self, data: OpenContract
    ) -> StatusFromOpenContract:
        tender = data.records[0].compiledRelease.tender
        return tender.status

    def get_tender_title_from_tender_ocds_data(self, data: OpenContract) -> str:
        tender = data.records[0].compiledRelease.tender
        return tender.title

    def get_tender_description_from_tender_ocds_data(self, data: OpenContract) -> str:
        tender = data.records[0].compiledRelease.tender
        return tender.description

    def get_tender_region_from_tender_ocds_data(self, data: OpenContract) -> Region:

        parties = data.records[0].compiledRelease.parties

        procuring_entities = [
            party for party in parties if PartyRoleEnum.PROCURING_ENTITY in party.roles
        ]

        if len(procuring_entities) != 1:
            raise ValueError(
                "There must be exactly one entity with the role of procuringEntity."
            )

        address = procuring_entities[0].address

        if address is None or address.region is None:
            raise ValueError(
                "The address or region is missing for the procuring entity."
            )

        return address.region

    def get_tender_tier(self, code: str) -> Tier:
        return Tier(code.split("-")[-1:][0][:2])

    def get_tender_status_from_image(self, html: str) -> StatusFromImage:
        status = self.get_src_by_element_id(html, "imgEstado")
        return StatusFromImage(status.split("/")[-1].replace(".png", "").upper())

    def get_tender_code_from_tender_ocds_data(self, data: OpenContract) -> str:
        return str(data.uri).split("/")[-1].strip()
