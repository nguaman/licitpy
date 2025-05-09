from typing import Dict, List

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
        """Initialize with the main application container."""
        self.country_providers = country_providers

    def get_tenders_by_codes(self, codes: List[str], country: Country) -> List[Tender]:
        """
        Get multiple tenders by their codes and country.
        This method is not implemented yet.
        """
        raise NotImplementedError("This method has not been implemented yet.")

    def _get_container_for_country(self, country: Country) -> CountryContainerProtocol:
        """
        Get the container for a specific country.
        Raises ValueError if the country is not supported.
        """
        country_container = self.country_providers.get(country)

        if country_container is None:
            raise ValueError(f"Country {country} is not supported.")

        return country_container

    def _get_tender_adapter(self, country: Country) -> TenderAdapter:
        """
        Get the tender adapter for a specific country.
        Raises ValueError if the country is not supported.
        """
        country_container = self._get_container_for_country(country)
        return country_container.tender_adapter()

    def get_tender_by_code(self, code: str, country: Country) -> Tender:

        adapter: TenderAdapter = self._get_tender_adapter(country)
        return Tender(code, country, adapter)

    async def aget_tender_by_code(self, code: str, country: Country) -> Tender:

        adapter: TenderAdapter = self._get_tender_adapter(country)
        return Tender(code, country, adapter)

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
