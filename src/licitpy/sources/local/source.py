from datetime import date, datetime
from typing import Any, AsyncIterable, AsyncIterator, Dict, Iterable, Iterator, List

from licitpy.core.containers.container import CountryContainerProtocol
from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country
from licitpy.core.interfaces.source import SourceProvider
from licitpy.core.interfaces.tender import TenderAdapter


class Local(SourceProvider):
    """
    Implementation of SourceProvider for local data sources.
    Uses country-specific providers to access tender information.
    """

    def __init__(
        self, country_providers: Dict[Country, CountryContainerProtocol]
    ) -> None:

        self.country_providers = country_providers

    def _get_container_for_country(self, country: Country) -> CountryContainerProtocol:
        """
        Retrieves the dependency injection container for a specific country.

        Args:
            country: The country for which to get the container.

        Returns:
            The CountryContainerProtocol for the specified country.

        Raises:
            ValueError: If the specified country is not supported (i.e., no
                        container is configured for it).
        """
        country_container = self.country_providers.get(country)

        if country_container is None:
            raise ValueError(f"Country {country} is not supported.")

        return country_container

    def _get_tender_adapter(self, country: Country) -> TenderAdapter:
        """
        Retrieves the tender adapter for a specific country.

        The adapter is responsible for fetching and parsing tender data for that country.

        Args:
            country: The country for which to get the tender adapter.

        Returns:
            An instance of TenderAdapter configured for the specified country.

        Raises:
            ValueError: If the specified country is not supported.
        """
        country_container = self._get_container_for_country(country)
        return country_container.tender_adapter()

    def get_tenders_by_codes(self, code: List[str], country: Country) -> List[Tender]:
        raise NotImplementedError(
            "get_tenders_by_codes is not implemented in Local source provider."
        )

    def get_tender_by_code(self, code: str, country: Country) -> Tender:
        """
        Retrieves a single tender object by its unique code and country.

        Args:
            code: The unique identification code of the tender.
            country: The country where the tender is located.

        Returns:
            A Tender object populated with data fetched via the country-specific adapter.
        """
        adapter: TenderAdapter = self._get_tender_adapter(country)
        return Tender(code, country, adapter)

    async def aget_tender_by_code(self, code: str, country: Country) -> Tender:
        """
        Asynchronously retrieves a single tender object by its unique code and country.

        Args:
            code: The unique identification code of the tender.
            country: The country where the tender is located.

        Returns:
            A Tender object populated with data fetched via the country-specific adapter.
        """
        adapter: TenderAdapter = self._get_tender_adapter(country)
        return Tender(code, country, adapter)

    async def afind_tenders(
        self, country: Country, filters: Dict[str, Any] = {}
    ) -> AsyncIterable[Tender]:

        # Select the country container based on the provided country
        adapter: TenderAdapter = self._get_tender_adapter(country)

        # If 'publication_on_date' is not explicitly provided in filters,
        # it defaults to the current day.
        publication_on_date: date = filters.get("publication_on_date", date.today())

        # If 'limit' is not explicitly provided in filters,
        # it defaults to None (no limit).
        limit = filters.get("limit", None)

        # Retrieve base tender codes by publication date.
        # These codes will serve as the initial set for subsequent filtering.
        codes: AsyncIterator[str] = adapter.aget_tenders_from_date(
            publication_on_date.year,
            publication_on_date.month,
            publication_on_date.day,
        )

        counter = 0
        async for code in codes:

            if limit is not None and counter >= limit:
                break

            # If a code passes all applied filters, a Tender object is yielded immediately.
            yield Tender(code, country, adapter)

            counter += 1

    def find_tenders(
        self, country: Country, filters: Dict[str, Any] = {}
    ) -> Iterable[Tender]:

        # Select the country container based on the provided country
        adapter: TenderAdapter = self._get_tender_adapter(country)

        # If 'publication_on_date' is not explicitly provided in filters,
        # it defaults to the current day.
        publication_on_date: date = filters.get("publication_on_date", date.today())

        # If 'limit' is not explicitly provided in filters,
        # it defaults to None (no limit).
        limit = filters.get("limit", None)

        # Retrieve base tender codes by publication date.
        # These codes will serve as the initial set for subsequent filtering.
        codes: Iterator[str] = adapter.get_tenders_from_date(
            publication_on_date.year,
            publication_on_date.month,
            publication_on_date.day,
        )

        # Iterate through the retrieved codes.
        # If a code passes all applied filters a Tender object is yielded immediately.
        counter = 0
        for code in codes:

            if limit is not None and counter >= limit:
                break

            yield Tender(code, country, adapter)

            counter += 1

    # def get_monthly_purchase_orders(
    #     self, start_date: date, end_date: date
    # ) -> PurchaseOrders:

    #     year_month: List[Tuple[int, int]] = []

    #     current_date = start_date
    #     while current_date <= end_date:

    #         year_month.append((current_date.year, current_date.month))
    #         current_date += relativedelta(months=1)

    #     purchase_orders: List[PurchaseOrderFromCSV] = []

    #     for year, month in year_month:

    #         purchase_orders += self.purchase_order_services.get_purchase_orders(
    #             year, month
    #         )

    #     return PurchaseOrders(
    #         [
    #             PurchaseOrder(
    #                 purchase_order.Codigo,
    #                 status=purchase_order.Estado,
    #                 title=purchase_order.Nombre,
    #                 issue_date=purchase_order.FechaEnvio,
    #                 region=purchase_order.RegionUnidadCompra,
    #                 commune=purchase_order.CiudadUnidadCompra,
    #                 services=self.purchase_order_services,
    #             )
    #             for purchase_order in purchase_orders
    #             if start_date <= purchase_order.FechaEnvio <= end_date
    #         ]
    #     )

    # def get_purchase_order(self, code: str) -> PurchaseOrder:
    #     return PurchaseOrder.create(code)

    # def get_tenders_by_status(self, status: Status) -> Tenders:
    #     return Tenders([])

    # def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:

    #     # 1) We get the range of months between the start and end dates (yyyy, mm)
    #     year_month: List[Tuple[int, int]] = []
    #     current_date = start_date

    #     while current_date <= end_date:

    #         # [(yyyy, mm), (yyyy, mm), ...]
    #         year_month.append((current_date.year, current_date.month))
    #         current_date += relativedelta(months=1)

    #     # 2) We retrieve the tenders from the sources (CSV files and API (OCDS))
    #     tenders_from_source: List[TenderFromSource] = []

    #     for year, month in year_month:
    #         tenders_from_source += self.tender_services.get_tenders_from_sources(
    #             year, month
    #         )

    #     # Filtering tenders that are internal QA tests from Mercado Publico.
    #     # eg: 500977-191-LS24 : Nombre Unidad : MpOperaciones
    #     tenders_from_source = [
    #         tender
    #         for tender in tenders_from_source
    #         if not tender.code.startswith("500977-")
    #     ]

    #     tenders: List[Tender] = []
    #     total = len(tenders_from_source)

    #     # 3) We verify the status of the tenders
    #     # We use the html of the tender to verify the status

    #     # for tender in tqdm(tenders_from_source, desc="Verifying tender status"):

    #     #     status, opening_date, region, closing_date = (
    #     #         self.tender_services.get_basics(tender.code)
    #     #     )

    #     #     tenders.append(
    #     #         Tender(
    #     #             tender.code,
    #     #             status=status,
    #     #             opening_date=opening_date,
    #     #             region=region,
    #     #             closing_date=closing_date,
    #     #             services=self.tender_services,
    #     #         )
    #     #     )

    #     with ThreadPoolExecutor(max_workers=32) as executor:

    #         futures_to_tender = {
    #             executor.submit(self.tender_services.get_basics, tender.code): tender
    #             for tender in tenders_from_source
    #         }

    #         for future in tqdm(
    #             as_completed(futures_to_tender),
    #             total=total,
    #             desc="Verifying tender status",
    #         ):

    #             tender = futures_to_tender[future]
    #             status, opening_date, region, closing_date = future.result()

    #             tenders.append(
    #                 Tender(
    #                     tender.code,
    #                     status=status,
    #                     opening_date=opening_date,
    #                     region=region,
    #                     closing_date=closing_date,
    #                     services=self.tender_services,
    #                 )
    #             )

    #     # 4) We retrieve only the tenders that fall within the requested date range
    #     return Tenders(
    #         [
    #             tender
    #             for tender in tenders
    #             if tender.opening_date
    #             and start_date <= tender.opening_date.date() <= end_date
    #         ]
    #     )
