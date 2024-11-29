from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import HttpUrl

from licitpy.services.tender import TenderServices
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Region, Tier
from licitpy.utils.validators import is_valid_public_market_code


class Tender:

    def __init__(
        self,
        code: str,
        region: Optional[Region] = None,
        status: Optional[Status] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        opening_date: Optional[date] = None,
        services: Optional[TenderServices] = None,
    ):

        if not is_valid_public_market_code(code):
            raise ValueError(f"Invalid public market code: {code}")

        self.code: str = code

        self._ocds: Optional[OpenContract] = None
        self._html: Optional[str] = None
        self._status: Optional[Status] = status
        self._url: Optional[HttpUrl] = None
        self._title: Optional[str] = title
        self._opening_date: Optional[date] = opening_date
        self._tier: Optional[Tier] = None
        self._description: Optional[str] = description
        self._region: Optional[Region] = region
        self._closing_date: Optional[datetime] = None

        self.services = services or TenderServices()

    @property
    def ocds(self) -> OpenContract:
        if self._ocds is None:
            self._ocds = self.services.get_ocds_data(self.code)
        return self._ocds

    @property
    def url(self) -> HttpUrl:
        if self._url is None:
            self._url = self.services.get_url(self.code)

        return self._url

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self.services.get_html(self.url)
        return self._html

    @property
    def opening_date(self) -> date:
        if self._opening_date is None:
            self._opening_date = self.services.get_opening_date(self.ocds)
        return self._opening_date

    @property
    def closing_date(self) -> datetime:
        if self._closing_date is None:
            self._closing_date = self.services.get_closing_date(self.ocds)
        return self._closing_date

    @property
    def is_open(self) -> bool:
        return self.services.is_open(self.closing_date)

    @property
    def status(self) -> Status:
        if self._status is None:
            self._status = self.services.get_status(self.ocds)
        return self._status

    @property
    def title(self) -> str:
        if self._title is None:
            self._title = self.services.get_title(self.ocds)
        return self._title

    @property
    def tier(self) -> Tier:
        if self._tier is None:
            self._tier = self.services.get_tier(self.code)
        return self._tier

    @property
    def description(self) -> str:
        if self._description is None:
            self._description = self.services.get_description(self.ocds)
        return self._description

    @property
    def region(self) -> Region:
        if self._region is None:
            self._region = self.services.get_region(self.ocds)
        return self._region

    @classmethod
    def create(cls, code: str) -> Tender:
        return cls(code)

    @classmethod
    def from_data(
        cls,
        code: str,
        *,
        region: Optional[Region] = None,
        status: Optional[Status] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        opening_date: Optional[date] = None,
    ) -> Tender:
        return cls(
            code,
            region=region,
            status=status,
            title=title,
            description=description,
            opening_date=opening_date,
        )
