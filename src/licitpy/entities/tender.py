from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import HttpUrl

from licitpy.services.tender import TenderServices
from licitpy.types import Status
from licitpy.types.tender import Tier


class Tender:

    def __init__(self, code: str, services: Optional[TenderServices] = None):

        self.code: str = code

        self._ocds: Optional[dict] = None
        self._html: Optional[str] = None
        self._status: Optional[Status] = None
        self._url: Optional[HttpUrl] = None
        self._title: Optional[str] = None
        self._opening_date: Optional[datetime] = None
        self._tier: Optional[str] = None

        self.services: TenderServices = services or TenderServices()

    @property
    def ocds(self) -> dict:
        if self._ocds is None:
            self._ocds = self.services.get_ocds_data(self.code)
        return self._ocds

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self.services.get_html(self.url)
        return self._html

    @property
    def status(self) -> Status:
        if self._status is None:
            self._status = self.services.get_status(self.ocds)
        return self._status

    @property
    def url(self) -> HttpUrl:
        if self._url is None:
            self._url = self.services.get_url(self.code)

        return self._url

    @property
    def title(self) -> str:
        if self._title is None:
            self._title = self.services.get_title(self.ocds)
        return self._title

    @property
    def opening_date(self) -> datetime:
        if self._opening_date is None:
            self._opening_date = self.services.get_opening_date(self.ocds)
        return self._opening_date

    @property
    def tier(self) -> Tier:
        if self._tier is None:
            self._tier = self.services.get_tier(self.code)
        return self._tier

    @classmethod
    def create(cls, code: str) -> Tender:
        return cls(code)
