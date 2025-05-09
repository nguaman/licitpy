from dependency_injector import containers, providers

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.sources.local.adapters.cl.parser import ChileTenderParser
from licitpy.sources.local.adapters.cl.adapter import ChileTenderAdapter

# from licitpy.sources.local.providers.co.tender_provider import ColombiaTenderAdapter
# from licitpy.sources.local.providers.eu.tender_provider import EuropeTenderAdapter


class ChileContainer(containers.DeclarativeContainer):
    """Contenedor para providers de tender por país."""

    # Configuración específica para tenders
    config = providers.Configuration()

    # Dependencias inyectadas desde el contenedor padre
    downloader: providers.Dependency[SyncDownloader] = providers.Dependency()
    adownloader: providers.Dependency[AsyncDownloader] = providers.Dependency()

    tender_adapter: providers.Factory[ChileTenderAdapter] = providers.Factory(
        ChileTenderAdapter,
        downloader=downloader,
        adownloader=adownloader,
        parser=providers.Singleton(ChileTenderParser),
    )

    # --- Placeholder: Providers para Purchase Order (PO) ---
    # po_parser: providers.Singleton[ChilePurchaseOrderParser] = providers.Singleton(
    #     ChilePurchaseOrderParser # Asumiendo que PO parser también es stateless
    # )
    #
    # po_adapter: providers.Factory[ChilePurchaseOrderAdapter] = providers.Factory(
    #     ChilePurchaseOrderAdapter, # Factory para aislamiento por operación de PO
    #     downloader=downloader,
    #     adownloader=adownloader,
    #     parser=po_parser, # Inyecta el parser específico de PO
    # )
