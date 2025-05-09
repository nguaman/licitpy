# Licitpy

**Licitpy** is a Python library designed to fetch and interact with public procurement data from different sources, starting with Chile's MercadoPublico.

## Project Structure

```markdown
.
├── CHANGELOG.md
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── tox.ini
└── src
    └── licitpy
        ├── __init__.py             # Makes licitpy a package
        ├── licitpy.py              # Main entry point class (Licitpy)
        ├── py.typed                # PEP 561 marker for type information
        ├── core
        │   ├── __init__.py
        │   ├── containers          # Dependency injection containers
        │   │   ├── __init__.py
        │   │   ├── chile.py        # DI container specific to Chile
        │   │   └── container.py    # Main DI container
        │   ├── downloader          # HTTP request handling (sync/async)
        │   │   ├── __init__.py
        │   │   ├── adownloader.py  # Async downloader implementation
        │   │   └── downloader.py   # Sync downloader implementation
        │   ├── entities            # Core data objects (e.g., Tender)
        │   │   ├── __init__.py
        │   │   └── tender.py       # Tender entity class
        │   ├── enums.py            # Enumerations (e.g., Country)
        │   ├── exceptions.py       # Custom exceptions
        │   ├── interfaces          # Abstract base classes/interfaces
        │   │   ├── __init__.py
        │   │   ├── source.py       # Interface for data sources
        │   │   └── tender.py       # Interface for tender adapters
        │   └── query.py            # Query builder class (TenderQuery)
        ├── examples                # Usage examples
        │   └── tender_url.py
        └── sources                 # Data source implementations
            ├── __init__.py
            ├── api                 # Implementation for a potential future API source
            │   ├── __init__.py
            │   └── source.py
            └── local               # Implementation for local/web-scraped sources
                ├── __init__.py
                ├── source.py       # Main class for the local source (Local)
                └── adapters        # Adapters for specific countries/platforms
                    ├── __init__.py
                    ├── cl          # Chile-specific adapter (MercadoPublico)
                    │   ├── __init__.py
                    │   ├── adapter.py    # ChileTenderAdapter implementation
                    │   ├── operations    # Helper functions for adapter logic
                    │   │   └── __init__.py
                    │   └── parser.py     # HTML/Data parser for Chile
                    ├── co          # Placeholder for Colombia
                    │   └── __init__.py
                    └── eu          # Placeholder for Europe
                        └── __init__.py
```





### Key Components Explanation

*   **`src/licitpy/`**: Main package directory.
    *   **`licitpy.py`**: Defines the main `Licitpy` class, the primary user entry point. Handles initialization, source selection, and context management (`async with`).
    *   **`py.typed`**: PEP 561 marker file indicating the package provides type information.

*   **`src/licitpy/core/`**: Contains the fundamental building blocks, interfaces, and business logic independent of specific data sources.
    *   **`containers/`**: Manages dependency injection using `dependency-injector`.
        *   `container.py`: The main container, sets up shared services (downloaders, config) and maps countries to sub-containers.
        *   `chile.py`: Sub-container for Chile-specific components (`ChileTenderAdapter`, `ChileTenderParser`).
    *   **`downloader/`**: Provides `SyncDownloader` and `AsyncDownloader` for HTTP requests with caching.
    *   **`entities/`**: Defines core data classes.
        *   `tender.py`: Represents a single tender, holding identity and an adapter for lazy data fetching.
    *   **`enums.py`**: Defines enumerations like `Country`.
    *   **`exceptions.py`**: Defines custom exception classes for the library.
    *   **`interfaces/`**: Defines abstract base classes (ABCs) or Protocols for consistency.
        *   `source.py`: `SourceProvider` interface.
        *   `tender.py`: `TenderAdapter` interface.
    *   **`query.py`**: `TenderQuery` class for building fluent queries (currently a placeholder).

*   **`src/licitpy/sources/`**: Contains implementations for different ways of getting data.
    *   **`api/`**: Placeholder for fetching data from a structured API.
    *   **`local/`**: Fetches data by directly interacting with source websites (e.g., web scraping).
        *   `source.py`: The `Local` class implements `SourceProvider`, selecting country adapters.
        *   **`adapters/`**: Contains country-specific logic.
            *   `cl/`: Chile-specific implementation (MercadoPublico).
                *   `adapter.py`: `ChileTenderAdapter` implements `TenderAdapter`, handling interaction logic.
                *   `parser.py`: `ChileTenderParser` handles parsing of MercadoPublico data.
                *   `operations/`: Contains helper functions extracted from the adapter.
            *   `co/`, `eu/`: Placeholders for other countries.

*   **`src/licitpy/examples/`**: Contains example scripts demonstrating library usage.

## Workflow Overview

1.  **Initialization**: User creates a `Licitpy` instance, selecting `API` or `Local` source.
2.  **Dependency Injection**: `Licitpy` initializes the main DI `Container`.
    *   Main `Container` sets up shared services (downloaders, config).
    *   Defines country sub-containers (e.g., `ChileContainer`) and injects shared services.
    *   Creates `country_providers` map (`Country` enum -> sub-container instance).
3.  **Source Provider Setup**:
    *   If `Local` source, `Licitpy` injects the resolved `country_providers` map into the `Local` instance.
4.  **Fetching Data (e.g., `get_tender_by_code`)**:
    *   User calls `licitpy.get_tender_by_code(code="...", country=Country.CL)`.
    *   Delegated to `Local.get_tender_by_code`.
    *   `Local` uses `country_providers` map to find `ChileContainer`.
    *   Calls `chile_container.tender_adapter()` to get `ChileTenderAdapter`.
    *   Creates `Tender` entity with `code`, `country`, and the `ChileTenderAdapter`.
5.  **Lazy Loading (e.g., `tender.url()`)**:
    *   User calls `tender.url()`.
    *   `Tender.url()` checks internal cache. If empty:
        *   Calls `self._adapter.get_tender_url(self.code)` (`ChileTenderAdapter` logic).
        *   `ChileTenderAdapter` uses `SyncDownloader` for HTTP requests.
        *   Processes response, returns URL.
    *   `Tender` caches and returns the URL.
6.  **Sync vs. Async**:
    *   Provides parallel sync (`get_...`, `.url()`) and async (`aget_...`, `.aurl()`) methods.
    *   Sync uses `SyncDownloader` (`requests`).
    *   Async uses `AsyncDownloader` (`aiohttp`), requiring context management (`async with Licitpy(...)`) or explicit `open/close`.
    *   DI injects the correct downloader type.
    *   Country selection via `country_providers` map is async-safe.

This structure promotes separation of concerns, extensibility for new countries, and robust sync/async handling.