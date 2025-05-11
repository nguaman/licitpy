from typing import Any, Dict, List

from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country
from licitpy.core.interfaces.source import SourceProvider


class API(SourceProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tender_by_code(self, code: str, country: Country) -> Tender:
        raise NotImplementedError("This method has not been implemented yet.")

    def get_tenders_by_codes(self, codes: List[str], country: Country) -> List[Tender]:
        raise NotImplementedError("This method has not been implemented yet.")

    async def aget_tender_by_code(self, code: str, country: Country) -> Tender:
        raise NotImplementedError("This method has not been implemented yet.")

    def find_tenders(
        self, country: Country, filters: Dict[str, Any] = {}
    ) -> List[Tender]:
        raise NotImplementedError("This method has not been implemented yet.")

    async def afind_tenders(
        self, country: Country, filters: Dict[str, Any] = {}
    ) -> List[Tender]:
        raise NotImplementedError("This method has not been implemented yet.")
