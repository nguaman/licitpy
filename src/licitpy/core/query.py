from datetime import date, datetime, timedelta
from typing import Any, AsyncIterable, AsyncIterator, Dict, Iterable, Iterator, List
from zoneinfo import ZoneInfo

from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country
from licitpy.core.exceptions import NonBusinessDayError
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

    def published_on(
        self, when: date | datetime | str, allow_weekends: bool = False
    ) -> "TenderQuery":
        """Filters tenders published on a specific date."""

        if not isinstance(when, (str, datetime, date)):
            raise TypeError(
                f"Invalid date type: {type(when)}. Expected string, datetime, or date."
            )

        if isinstance(when, str):
            try:
                when = datetime.strptime(when, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"Invalid date format: {when}. Expected format is YYYY-MM-DD."
                )

        elif isinstance(when, datetime):
            if when.tzinfo is None:
                raise ValueError(
                    f"Date is naive and lacks timezone information: {when}. "
                    "Please provide a timezone-aware datetime."
                )

            when = when.date()

        # Check if the date is in the future
        if when > datetime.now(ZoneInfo("UTC")).date():
            raise ValueError(
                f"Date cannot be in the future: {when}. Please provide a valid date."
            )

        # Check if the date is a weekend (Saturday or Sunday)
        if when.weekday() >= 5 and not allow_weekends:
            raise NonBusinessDayError(
                f"Date {when} is a weekend. If you still want to search on weekends, "
                f"set allow_weekends=True in your published_on() call."
            )

        self._filters["publication_on_date"] = when

        return self

    def published_today(self) -> "TenderQuery":
        """Filters tenders published today (UTC)."""
        today_utc = datetime.now(ZoneInfo("UTC")).date()
        return self.published_on(today_utc)

    def published_yesterday(self) -> "TenderQuery":
        """Filters tenders published yesterday (UTC)."""
        yesterday_utc = datetime.now(ZoneInfo("UTC")).date() - timedelta(days=1)
        return self.published_on(yesterday_utc)

    # def published_between(self, start_date: Any, end_date: Any) -> "TenderQuery":
    #     """Filters tenders published between start_date and end_date (inclusive)."""
    #     self._filters[QueryFilter.PUBLICATION_DATE_RANGE] = (start_date, end_date)
    #     print(f"Query: Added publication date range filter: {start_date} to {end_date}")
    #     return self

    # def closing_between(self, start_date: Any, end_date: Any) -> "TenderQuery":
    #     """Filters tenders closing between start_date and end_date (inclusive)."""
    #     self._filters[QueryFilter.CLOSING_DATE_RANGE] = (start_date, end_date)
    #     print(f"Query: Added closing date range filter: {start_date} to {end_date}")
    #     return self

    # def closing_after(self, date: Any) -> "TenderQuery":
    #     """Filters tenders closing after a specific date."""
    #     self._filters[QueryFilter.CLOSING_AFTER_DATE] = date
    #     print(f"Query: Added closing after date filter: {date}")
    #     return self

    # def closing_before(self, date: Any) -> "TenderQuery":
    #     """Filters tenders closing before a specific date."""
    #     self._filters[QueryFilter.CLOSING_BEFORE_DATE] = date
    #     print(f"Query: Added closing before date filter: {date}")
    #     return self

    # def closing_on(self, when: Any) -> "TenderQuery":
    #     """Filters tenders closing on a specific date."""
    #     self._filters["closing_on_date"] = when
    #     print(f"Query: Added closing on date filter: {when}")
    #     return self

    # def by_budget_tier(self, tier: Any) -> "TenderQuery":
    #     self._filters[QueryFilter.BUDGET_TIER] = tier
    #     print(f"Query: Added budget filter: {tier}")
    #     return self

    # def with_status(self, status: str) -> "TenderQuery":
    #     print(f"Query: Adding status filter: {status}")
    #     self._filters[QueryFilter.STATUS] = status
    #     return self

    # def in_region(self, region: Any) -> "TenderQuery":
    #     """Filters tenders by geographical region."""
    #     self._filters[QueryFilter.REGION] = region
    #     print(f"Query: Added region filter: {region}")
    #     return self

    # def with_keyword(self, keyword: str) -> "TenderQuery":
    #     """Filters tenders by a keyword search in their content."""
    #     self._filters[QueryFilter.KEYWORD_SEARCH] = keyword
    #     print(f"Query: Added keyword filter: {keyword}")
    #     return self

    # def for_industry_sector(self, sector_identifier: str) -> "TenderQuery":
    #     """Filters tenders by industry sector or category."""
    #     self._filters[QueryFilter.INDUSTRY_SECTOR] = sector_identifier
    #     print(f"Query: Added industry sector filter: {sector_identifier}")
    #     return self

    # def from_buyer_entity(self, entity_identifier: str) -> "TenderQuery":
    #     """Filters tenders by the buyer entity (public organism)."""
    #     self._filters[QueryFilter.BUYER_ENTITY] = entity_identifier
    #     print(f"Query: Added buyer entity filter: {entity_identifier}")
    #     return self

    def limit(self, count: int) -> "TenderQuery":
        print(f"Query: Adding limit: {count}")

        self._filters["limit"] = count
        return self

    async def __aiter__(self) -> AsyncIterator[Tender]:
        print("Query: __aiter__() called (lazy execution)")

        # If no publication date filter is explicitly set,
        # default to filtering tenders published today (UTC).
        if "publication_on_date" not in self._filters:
            self._filters["publication_on_date"] = datetime.now(ZoneInfo("UTC")).date()

        async for tender in self._source.afind_tenders(
            country=self._country, filters=self._filters
        ):
            yield tender

    def __iter__(self) -> Iterable[Tender]:
        print("Query: __iter__() called (lazy execution)")

        # If no publication date filter is explicitly set,
        # default to filtering tenders published today (UTC).
        if "publication_on_date" not in self._filters:
            self._filters["publication_on_date"] = datetime.now(ZoneInfo("UTC")).date()

        yield from self._source.find_tenders(
            country=self._country, filters=self._filters
        )

    def all(self) -> Iterator[Tender]:
        print("Query: .all() called (processing incrementally)")
        return self.stream()

    def collect(self) -> List[Tender]:
        """
        Waits for all results before returning them as a complete list.
        Warning: May consume significant memory for large result sets.
        """
        print("Query: .collect() called (waiting for all results)")
        return list(self.__iter__())

    def stream(self) -> Iterator[Tender]:
        """
        Default method to access results - returns tenders incrementally as they're processed.
        """
        print("Query: .stream() called (processing incrementally)")
        yield from self.__iter__()

    async def astream(self) -> AsyncIterator[Tender]:
        """
        Default async method to access results - yields tenders incrementally as they're processed.
        This is the recommended way to handle large result sets asynchronously.

        Example:
            async for tender in query.astream():
                await process_tender(tender)
        """
        print("Query: .astream() called (async incremental processing)")
        async for tender in self:
            yield tender

    async def acollect(self) -> List[Tender]:
        """
        Asynchronously waits for all results before returning them as a complete list.
        Warning: May consume significant memory for large result sets.
        """
        print("Query: .acollect() called (async materializing all results)")
        return [tender async for tender in self]

    async def aall(self) -> AsyncIterator[Tender]:
        """
        Returns tenders incrementally (same as astream())
        Use acollect() if you need all results as a complete list.
        """
        print("Query: .aall() called (async incremental processing)")
        async for tender in self.astream():
            yield tender
