from datetime import date
from typing import List, Optional, Tuple

from dateutil.relativedelta import relativedelta

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.services.tender import TenderServices
from licitpy.sources.base import BaseSource
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import TenderFromCSV


class Local(BaseSource):
    def __init__(self, service: Optional[TenderServices] = None) -> None:
        self.service = service or TenderServices()

    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:

        year_month: List[Tuple[int, int]] = []

        current_date = start_date
        while current_date <= end_date:

            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        tenders: List[TenderFromCSV] = []

        for year, month in year_month:
            tenders += self.service.get_tenders(year, month)

        return Tenders.from_tenders(
            [
                Tender(
                    tender.CodigoExterno,
                    region=tender.RegionUnidad,
                    status=Status(tender.Estado.name),
                    title=tender.Nombre,
                    description=tender.Descripcion,
                    opening_date=tender.FechaPublicacion,
                )
                for tender in tenders
                if start_date <= tender.FechaPublicacion <= end_date
            ]
        )

    def get_tender(self, code: str) -> Tender:
        return Tender.create(code)
