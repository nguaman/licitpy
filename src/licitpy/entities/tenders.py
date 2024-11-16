from __future__ import annotations

from operator import attrgetter
from typing import List

from licitpy.entities.tender import Tender
from licitpy.types import Status, Tier
from licitpy.utils.threads import execute_concurrently


class Tenders:
    def __init__(self, tenders: List[Tender]):
        self._tenders = sorted(tenders, key=attrgetter("code"), reverse=True)

    def by_budget_tier(self, tier: Tier) -> Tenders:
        return Tenders([tender for tender in self._tenders if tender.tier == tier])

    def with_status(self, status: Status) -> Tenders:

        tenders: List[Tender] = execute_concurrently(
            function=lambda tender: tender.status == status,
            items=self._tenders,
            desc=f"Filtering tenders by status {status}",
        )

        return Tenders(tenders)

    def to_pandas(self):
        raise NotImplementedError

    @classmethod
    def create(cls, codes: List[str]) -> Tenders:
        return cls([Tender.create(code) for code in codes])

    @property
    def codes(self) -> List[str]:
        return [tender.code for tender in self._tenders]

    def limit(self, limit: int) -> Tenders:
        return Tenders(self._tenders[:limit])

    def count(self) -> int:
        return len(self._tenders)

    def __iter__(self):
        return iter(self._tenders)
