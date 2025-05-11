import base64
from datetime import timedelta

from pydantic import HttpUrl
from requests import Response, Session
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

    def download_file_to_base64(self, url: HttpUrl) -> str:

        response = self.session.get(str(url), stream=True)
        response.raise_for_status()

        file_content = bytearray()

        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file_content.extend(chunk)

        base64_content = base64.b64encode(file_content).decode("utf-8")

        return base64_content
