from datetime import timedelta
from requests import Session
from requests_cache import CachedSession



class SyncDownloader:
    """Handles synchronous HTTP requests with optional caching."""

    def __init__(self, use_cache: bool, cache_expire_after: timedelta) -> None:
        """
        Initialize the downloader and create the session immediately.
        
        Unlike async resources that should be explicitly opened/closed, 
        sync resources can be safely initialized at creation time.
        """
        self._use_cache = use_cache
        self._cache_expire_after = cache_expire_after
        self.session: Session | CachedSession

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en,es-ES;q=0.9,es;q=0.8",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }

        if use_cache:
            self.session = CachedSession(
                cache_name="licitpy_sync",
                backend="sqlite",
                expire_after=cache_expire_after,
                allowable_methods=["GET", "POST", "HEAD"],
                stale_if_error=True,
                allowable_codes=[200, 302],
                cache_control=False,
                fast_save=False,
            )
        else:
            self.session = Session()

        self.session.headers.update(self.headers)

    def open(self) -> None:
        """
        No-op method to maintain API consistency with AsyncDownloader.
        
        This method exists to provide a consistent interface between sync and async
        resources, even though sync resources are initialized in __init__.
        
        This pattern allows the public API to be consistent: both sync and async 
        versions can be used with the same pattern (`downloader.open()`), which
        simplifies usage and maintains compatibility with context managers.
        """
        pass

    def close(self) -> None:
        """Closes the synchronous session."""
        if self.session:
            self.session.close()
