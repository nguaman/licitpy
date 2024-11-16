import base64

from pydantic import HttpUrl
from requests import Response, Session
from requests_cache import CachedSession
from tenacity import retry, stop_after_attempt, wait_incrementing
from tqdm import tqdm

from licitpy.settings import settings


class BaseDownloader:
    """
    A base class for handling HTTP requests and downloading files with optional caching.

    Attributes:
        session (requests.Session or CachedSession): The HTTP session used for making requests.
    """

    def __init__(self) -> None:
        """
        Initializes the BaseDownloader instance.

        If caching is enabled in the settings, it uses a `CachedSession` for requests.
        Otherwise, it defaults to a standard `Session`.

        The session is pre-configured with default headers for web navigation.
        """

        if settings.use_cache:
            self.session = CachedSession(
                cache_name="licitpy",
                backend="sqlite",
                expire_after=settings.cache_expire_after,
                allowable_methods=["GET", "POST", "HEAD"],
                stale_if_error=True,
                allowable_codes=[200, 302],
                cache_control=False,
                fast_save=False,
            )
        else:
            self.session = Session()

        self.session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en,es-ES;q=0.9,es;q=0.8",
                "Connection": "keep-alive",
                "DNT": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
            }
        )

    def get_html_from_url(self, url: HttpUrl) -> str:
        """
        Fetches the HTML content from a given URL.

        Args:
            url (HttpUrl): The URL to fetch the HTML content from.

        Returns:
            str: The HTML content of the response, decoded as UTF-8.
        """
        return self.session.get(url).content.decode("utf-8")

    @retry(stop=stop_after_attempt(3), wait=wait_incrementing(start=3, increment=3))
    def download_file_base64(
        self,
        response: Response,
        file_size: int,
        file_name: str,
    ) -> str:
        """
        Downloads a file from a response stream and encodes it as a base64 string.

        This method supports large file downloads with progress tracking and retries
        on failure using the `tenacity` library.

        Args:
            response (Response): The HTTP response object containing the file data.
            file_size (int): The total size of the file in bytes.
            file_name (str): The name of the file being downloaded (used for progress description).

        Returns:
            str: The base64-encoded string of the downloaded file content.
        """

        file_content = bytearray()

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {file_name}",
            disable=settings.disable_progress_bar,
        ) as progress_bar:

            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_content.extend(chunk)
                    progress_bar.update(len(chunk))
                    progress_bar.refresh()

        base64_content = base64.b64encode(file_content).decode("utf-8")

        return base64_content
