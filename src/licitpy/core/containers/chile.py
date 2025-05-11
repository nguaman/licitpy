"""
Dependency Injection container for Chile-specific components.

This module defines a container that manages the creation and wiring of
dependencies specifically required for handling Chilean tender data. It uses
the `dependency-injector` library to achieve this.
"""

from dependency_injector import containers, providers

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.sources.local.adapters.cl.adapter import ChileTenderAdapter
from licitpy.sources.local.adapters.cl.parser import ChileTenderParser
from licitpy.sources.local.adapters.cl.services.tender_aggregator import (
    ChileanTenderAggregatorService,
)


class ChileContainer(containers.DeclarativeContainer):
    """
    Manages dependencies for Chilean tender data handling.
    Provides configured instances of services like adapters and parsers.
    """

    # Configuration provider.
    # Allows for runtime configuration of components within this container.
    config = providers.Configuration()

    # Dependency for a synchronous HTTP downloader.
    # This will be injected from a parent container.
    downloader: providers.Dependency[SyncDownloader] = providers.Dependency()

    # Dependency for an asynchronous HTTP downloader.
    # This will be injected from a parent container.
    adownloader: providers.Dependency[AsyncDownloader] = providers.Dependency()

    # Service for aggregating tender data from multiple Chilean sources (e.g., CSV, API).
    # It consolidates and deduplicates tender information for initial queries.
    tender_aggregator: providers.Singleton[ChileanTenderAggregatorService] = (
        providers.Singleton(
            ChileanTenderAggregatorService,
            downloader=downloader,
            adownloader=adownloader,
        )
    )

    # Factory for ChileTenderAdapter.
    # Creates ChileTenderAdapter instances with injected downloaders and parser.
    tender_adapter: providers.Factory[ChileTenderAdapter] = providers.Factory(
        ChileTenderAdapter,
        downloader=downloader,
        adownloader=adownloader,
        parser=providers.Singleton(ChileTenderParser),
        data=tender_aggregator,
    )
