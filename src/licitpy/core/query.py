from typing import Any, Dict, Iterable, List

from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country
from licitpy.core.interfaces.source import SourceProvider


class TenderQuery:

    def __init__(self, source: SourceProvider, country: Country):
        self._source = source
        self._country = country
        self._filters: Dict[str, Any] = {}

    """
    Represents a query for tenders that can be built using a fluent interface.
    The query is executed lazily when results are requested (e.g., via iteration or .all()).
    """

    def from_date(self, time_range: Any) -> "TenderQuery":
        """Adds a date filter to the query."""
        # Placeholder: Store or process time_range into date filters
        self._filters["time_range"] = time_range
        print(f"Query: Added date filter: {time_range}")
        return self

    def by_budget_tier(self, tier: Any) -> "TenderQuery":
        """Adds a budget tier filter to the query."""
        self._filters["budget_tier"] = tier
        print(f"Query: Added budget filter: {tier}")
        return self

    def with_status(self, status: str) -> "TenderQuery":
        """Placeholder to filter by status."""
        print(f"Query: Adding status filter: {status}")
        self._filters["status"] = status
        return self

    def limit(self, count: int) -> "TenderQuery":
        """Placeholder to limit the number of results."""
        print(f"Query: Adding limit: {count}")
        self._limit = count
        return self

    # def __iter__(self) -> Iterable[Tender]:
    #     ...
    # AQUI ES DONDE SE EJEUTA TODO! cuando se hace un loop o algo
    # #     """Placeholder for implicit synchronous execution."""
    # #     print("Query: __iter__ called (sync execution)")
    # #     # Aquí se llamaría a self._source.find_tenders(...)
    # #     # yield from self._source.find_tenders(
    # #     #      country=self._country,
    # #     #      filters=self._filters,
    # #     #      limit=self._limit,
    # #     #      order_by=self._order_by
    # #     #  )
    # #     # pass # Eliminar pass cuando se implemente yield from

    # def all(self) -> List[Tender]:
    #      """Placeholder for explicit synchronous execution."""
    #      print("Query: .all() called (sync execution)")
    #      # Aquí se llamaría a self._source.find_tenders(...) y se convertiría a lista
    #      return list(self.__iter__())
    #      # pass # Eliminar pass cuando se implemente list()
