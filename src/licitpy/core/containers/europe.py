"""
Dependency Injection container for Chile-specific components.

This module defines a container that manages the creation and wiring of
dependencies specifically required for handling Chilean tender data. It uses
the `dependency-injector` library to achieve this.
"""

from dependency_injector import containers, providers

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.sources.local.adapters.eu.parser import EuropeTenderParser
from licitpy.sources.local.adapters.eu.adapter import EuropeTenderAdapter


class EuropeContainer(containers.DeclarativeContainer):
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

    # Factory for EuropeTenderAdapter.
    # Creates EuropeTenderAdapter instances with injected downloaders and parser.
    tender_adapter: providers.Factory[EuropeTenderAdapter] = providers.Factory(
        EuropeTenderAdapter,
        downloader=downloader,  # Injects the sync downloader
        adownloader=adownloader,  # Injects the async downloader
        parser=providers.Singleton(
            EuropeTenderParser
        ),  # Injects a singleton instance of the parser
    )
