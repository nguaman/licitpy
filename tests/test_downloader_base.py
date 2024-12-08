import base64
import random
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest
from pydantic import HttpUrl
from requests import Response, Session
from requests_cache import CachedSession

from licitpy.downloader.base import BaseDownloader
from licitpy.settings import settings
from pytest_mock import MockerFixture


@pytest.fixture
def base_downloader() -> BaseDownloader:
    """Returns a BaseDownloader instance"""
    return BaseDownloader()


def test_init_with_cache(base_downloader: BaseDownloader) -> None:
    """Test the initialization of the BaseDownloader with cache"""
    settings.use_cache = True
    assert isinstance(base_downloader.session, CachedSession)


def test_init_without_cache(base_downloader: BaseDownloader) -> None:
    """Test the initialization of the BaseDownloader without cache"""
    settings.use_cache = False
    assert isinstance(base_downloader.session, Session)


EXPECTED_HEADERS: Dict[str, str] = {
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


def test_session_headers(base_downloader: BaseDownloader) -> None:
    """Test the headers of the BaseDownloader session."""
    headers = base_downloader.session.headers
    for key, expected_value in EXPECTED_HEADERS.items():
        assert key in headers, f"Header '{key}' not found in session headers."
        assert (
            headers[key] == expected_value
        ), f"Header '{key}' has an unexpected value."


def test_get_html_from_url(
    base_downloader: BaseDownloader, mocker: MockerFixture
) -> None:
    """Test the get_html_from_url method of the BaseDownloader."""

    expected_html_content: str = "<html><body><h1>Licitpy</h1></body></html>"
    url = HttpUrl("https://example.com")

    mock_response = MagicMock(spec=Response)
    mock_response.content.decode.return_value = expected_html_content

    mock_get = mocker.patch.object(
        base_downloader.session, "get", return_value=mock_response
    )

    result = base_downloader.get_html_from_url(url)

    mock_get.assert_called_once_with(str(url))

    assert (
        result == expected_html_content
    ), f"Expected HTML content '{expected_html_content}', but got '{result}'."


def test_download_file_base64(base_downloader: BaseDownloader) -> None:
    """Test the download_file_base64 method of the BaseDownloader."""

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
    """Test the download_file_base64 method of the BaseDownloader with empty chunks."""

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
