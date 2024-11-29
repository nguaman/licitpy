from unittest.mock import MagicMock

import pytest

from licitpy.types.attachments import Attachment, ContentStatus, FileType


@pytest.fixture
def mock_download_fn() -> MagicMock:
    return MagicMock(return_value="file content")


@pytest.fixture
def attachment(mock_download_fn: MagicMock) -> Attachment:
    return Attachment(
        id="1",
        name="test_file.pdf",
        type="text",
        description="A test file",
        size=1024,
        upload_date="2024-01-01",
        file_type=FileType.PDF,
        _download_fn=mock_download_fn,
    )


def test_attachment_initial_status(attachment: Attachment) -> None:
    assert attachment.content_status == ContentStatus.PENDING_DOWNLOAD


def test_attachment_content_download(
    attachment: Attachment, mock_download_fn: MagicMock
) -> None:

    attachment._download_fn = mock_download_fn

    content = attachment.content
    assert content == "file content"

    assert attachment.content_status == ContentStatus.AVAILABLE

    mock_download_fn.assert_called_once()


def test_attachment_content_cached(
    attachment: Attachment, mock_download_fn: MagicMock
) -> None:

    attachment._download_fn = mock_download_fn

    # This will trigger the download for the first time
    _ = attachment.content

    # This will not trigger the download
    content = attachment.content

    # The content should be the same
    assert content == "file content"

    mock_download_fn.assert_called_once()
