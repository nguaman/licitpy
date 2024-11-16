from datetime import date
from typing import Dict, List, Optional, Tuple

from dateutil.relativedelta import relativedelta

from licitpy.entities.tenders import Tenders
from licitpy.services.tender import TenderServices


class Local:
    def __init__(self, service: Optional[TenderServices] = None) -> None:
        self.service: TenderServices = service or TenderServices()

    def get_monthly_tenders(self, start_date: date, end_date: date):

        year_month: List[Tuple[int, int]] = []

        current_date = start_date
        while current_date <= end_date:

            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        tenders: List[Dict[str, str]] = []

        for year, month in year_month:
            tenders += self.service.get_tender_codes(year, month)

        return Tenders.create(
            [
                tender["CodigoExterno"]
                for tender in tenders
                if start_date <= tender["FechaPublicacion"] <= end_date
            ]
        )
