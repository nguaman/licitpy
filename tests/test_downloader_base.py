import base64
from unittest.mock import MagicMock, Mock, patch

import pytest
from pydantic import HttpUrl
from requests import Response, Session
from requests_cache import CachedSession

from licitpy.downloader.base import BaseDownloader
from licitpy.settings import settings


@pytest.fixture
def base_downloader() -> BaseDownloader:
    return BaseDownloader()


def test_init_with_cache(base_downloader: BaseDownloader) -> None:
    settings.use_cache = True
    downloader = BaseDownloader()
    assert isinstance(downloader.session, CachedSession)


def test_init_without_cache(base_downloader: BaseDownloader) -> None:
    settings.use_cache = False
    downloader = BaseDownloader()
    assert isinstance(downloader.session, Session)


def test_session_headers(base_downloader: BaseDownloader) -> None:
    """Prueba que las cabeceras de la sesión se actualizan correctamente."""
    headers = base_downloader.session.headers
    assert (
        headers["Accept"]
        == "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    )
    assert headers["Accept-Language"] == "en,es-ES;q=0.9,es;q=0.8"
    assert headers["Connection"] == "keep-alive"
    assert headers["DNT"] == "1"
    assert headers["Sec-Fetch-Dest"] == "document"
    assert headers["Sec-Fetch-Mode"] == "navigate"
    assert headers["Sec-Fetch-Site"] == "none"
    assert headers["Sec-Fetch-User"] == "?1"
    assert headers["Upgrade-Insecure-Requests"] == "1"
    assert (
        headers["User-Agent"]
        == "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
    assert (
        headers["sec-ch-ua"]
        == '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"'
    )
    assert headers["sec-ch-ua-mobile"] == "?0"
    assert headers["sec-ch-ua-platform"] == '"Linux"'


def test_get_html_from_url(base_downloader: BaseDownloader) -> None:
    html_content = "<html><body><h1>Licitpy</h1></body></html>"
    mock_response = MagicMock()
    mock_response.content.decode.return_value = html_content

    with patch.object(
        base_downloader.session, "get", return_value=mock_response
    ) as mock_get:
        url = HttpUrl("https://example.com")
        result = base_downloader.get_html_from_url(url)

        mock_get.assert_called_once_with(str(url))
        assert result == html_content


def test_download_file_base64(base_downloader: BaseDownloader) -> None:
    mock_response = Mock(spec=Response)
    mock_response.iter_content = MagicMock(
        return_value=[b"chunk1", b"chunk2", b"chunk3"]
    )
    mock_response.headers = {"Content-Length": "18"}

    file_size = 18
    file_name = "test_file"

    base64_content = base_downloader.download_file_base64(
        mock_response, file_size, file_name
    )

    expected_base64_content = base64.b64encode(b"chunk1chunk2chunk3").decode("utf-8")
    assert base64_content == expected_base64_content


def test_download_file_base64_with_empty_chunks(
    base_downloader: BaseDownloader,
) -> None:
    mock_response = Mock(spec=Response)
    mock_response.iter_content = MagicMock(
        return_value=[b"chunk1", b"", b"chunk2", b"", b"chunk3"]
    )
    file_size = 18
    file_name = "test_file"

    base64_content = base_downloader.download_file_base64(
        mock_response, file_size, file_name
    )

    expected_content = b"chunk1chunk2chunk3"
    expected_base64_content = base64.b64encode(expected_content).decode("utf-8")
    assert base64_content == expected_base64_content
