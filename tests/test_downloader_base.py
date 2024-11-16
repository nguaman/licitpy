import base64
from unittest.mock import MagicMock, patch

import pytest
from requests import Response, Session
from requests_cache import CachedSession

from licitpy.downloader.base import BaseDownloader


@pytest.fixture
def downloader():
    """Fixture for creating a BaseDownloader instance."""
    return BaseDownloader()


@pytest.fixture
def mock_response():
    """Fixture for mocking a Response object."""
    mock = MagicMock(spec=Response)
    mock.iter_content = MagicMock(return_value=[b"chunk1", b"chunk2"])
    return mock


def test_base_downloader_with_cache():
    """Test that BaseDownloader uses CachedSession when caching is enabled."""
    with patch("licitpy.downloader.base.settings.use_cache", True):
        downloader = BaseDownloader()
        assert isinstance(
            downloader.session, CachedSession
        ), "Expected CachedSession when caching is enabled."


def test_base_downloader_without_cache():
    """Test that BaseDownloader uses regular Session when caching is disabled."""
    with patch("licitpy.downloader.base.settings.use_cache", False):
        downloader = BaseDownloader()
        assert isinstance(
            downloader.session, Session
        ), "Expected Session when caching is disabled."


def test_get_html_from_url(downloader):
    """Test that BaseDownloader can fetch and return HTML content from a URL."""
    # Mock the session's get method to return predefined content
    downloader.session.get = MagicMock(
        return_value=MagicMock(content=b"<html>LicitPy</html>")
    )

    url = "http://licitpy.dev"
    html = downloader.get_html_from_url(url)

    assert (
        html == "<html>LicitPy</html>"
    ), "Expected the HTML content to match the mocked response."
    downloader.session.get.assert_called_once_with(url)


def test_download_file_base64(downloader, mock_response):
    """Test that BaseDownloader correctly downloads and encodes a file as base64."""
    file_size = 164
    file_name = "attachment.pdf"

    # Mock tqdm to avoid actual progress bar display during tests
    with patch("licitpy.downloader.base.tqdm", MagicMock()):
        base64_content = downloader.download_file_base64(
            response=mock_response, file_size=file_size, file_name=file_name
        )

    expected_base64 = base64.b64encode(b"chunk1chunk2").decode("utf-8")
    assert (
        base64_content == expected_base64
    ), "Expected base64-encoded content to match."
    mock_response.iter_content.assert_called_once_with(chunk_size=8192)
