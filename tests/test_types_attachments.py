from unittest.mock import MagicMock

import pytest

from licitpy.types.attachments import Attachment, ContentStatus


@pytest.fixture
def mock_download_fn() -> MagicMock:
    return MagicMock(return_value=("text/plain", "file content"))


@pytest.fixture
def attachment(mock_download_fn: MagicMock) -> Attachment:
    return Attachment(
        id="1",
        name="test_file",
        type="text",
        description="A test file",
        size=1024,
        upload_date="2024-01-01",
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


def test_attachment_file_type_resolves_correctly(
    attachment: Attachment, mock_download_fn: MagicMock
) -> None:

    mock_download_fn.return_value = ("text/plain", "file content")
    attachment._download_fn = mock_download_fn

    assert attachment.file_type == "text/plain"

    mock_download_fn.assert_called_once()


def test_attachment_file_type_raises_error_when_missing(
    attachment: Attachment, mock_download_fn: MagicMock
) -> None:
    """
    Verifica que se lanza un ValueError si el tipo de archivo no se puede determinar.
    """
    mock_download_fn.return_value = (None, "file content")
    attachment._download_fn = mock_download_fn

    with pytest.raises(
        ValueError, match="File type could not be determined after content download."
    ):
        _ = attachment.file_type
