"""
Core application container.

This module defines the root dependency injection container for the application,
which orchestrates all services and their dependencies.
"""

from typing import Any, Dict, Protocol
from dependency_injector import containers, providers

from licitpy.core.containers.chile import ChileContainer
from licitpy.core.containers.europe import EuropeContainer
from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader
from licitpy.core.enums import Country
from licitpy.sources.local.adapters.cl.adapter import ChileTenderAdapter


class CountryContainerProtocol(Protocol):
    tender_adapter: providers.Factory[ChileTenderAdapter]


class Container(containers.DeclarativeContainer):
    """Root container for the application."""

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(packages=["licitpy"])

    downloader: providers.Singleton[SyncDownloader] = providers.Singleton(
        SyncDownloader,
        use_cache=config.use_cache,
        cache_expire_after=config.cache_expire_after,
    )

    adownloader: providers.Singleton[AsyncDownloader] = providers.Singleton(
        AsyncDownloader,
        use_cache=config.use_cache,
        cache_expire_after=config.cache_expire_after,
    )

    cl_config = providers.Configuration()

    cl = providers.Container(
        ChileContainer,
        config=cl_config,
        downloader=downloader,
        adownloader=adownloader,
    )

    eu_config = providers.Configuration()
    
    eu = providers.Container(
        EuropeContainer,
        config=eu_config,
        downloader=downloader,
        adownloader=adownloader,
    )

    country_providers: providers.Provider[Dict[Country, CountryContainerProtocol]] = (
        providers.Dict(
            {
                Country.CL: cl,
                Country.EU: eu,
            }
        )
    )
