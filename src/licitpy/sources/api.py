from datetime import date

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders


class API:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:
        raise NotImplementedError("This method has not been implemented yet.")

    def get_tender(self, code: str) -> Tender:
        raise NotImplementedError("This method has not been implemented yet.")
