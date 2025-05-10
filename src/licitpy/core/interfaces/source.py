import logging
from abc import ABC, abstractmethod
from typing import List

from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country


class SourceProvider(ABC):

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    # @abstractmethod
    # def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:
    #     pass  # pragma: no cover

    @abstractmethod
    async def aget_tender_by_code(self, code: str, country: Country) -> Tender:
        """Asynchronously retrieves a single tender object by its unique code."""
        pass  # pragma: no cover

    @abstractmethod
    def get_tender_by_code(self, code: str, country: Country) -> Tender:
        pass  # pragma: no cover

    @abstractmethod
    def get_tenders_by_codes(self, code: List[str], country: Country) -> List[Tender]:
        pass  # pragma: no cover

    # @abstractmethod
    # def get_purchase_order(self, code: str) -> PurchaseOrder:
    #     pass  # pragma: no cover

    # @abstractmethod
    # def get_tenders_by_status(self, status: Status) -> Tenders:
    #     pass  # pragma: no cover
