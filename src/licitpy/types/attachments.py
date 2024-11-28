from enum import Enum
from typing import Callable, Optional

from pydantic import BaseModel, PrivateAttr


class ContentStatus(Enum):
    """
    Enum representing the content's download status.

    Attributes:
        PENDING_DOWNLOAD: Content is ready to be downloaded. Access `.content` to trigger the download.
        AVAILABLE: Content has been downloaded and is ready to use.
    """

    PENDING_DOWNLOAD = "Pending download"
    AVAILABLE = "Downloaded"


class Attachment(BaseModel):
    id: str
    name: str
    type: str
    description: str
    size: int
    upload_date: str
    _file_type: Optional[str] = PrivateAttr(default=None)
    _download_fn: Callable[[], tuple[str, str]] = PrivateAttr()
    _content: Optional[str] = PrivateAttr(default=None)

    @property
    def content(self) -> Optional[str]:
        self._file_type, self._content = self._download_fn()
        return self._content

    @property
    def file_type(self) -> str:
        if self._file_type is None:
            _ = self.content

        if self._file_type is None:
            raise ValueError(
                "File type could not be determined after content download."
            )

        return self._file_type

    @property
    def content_status(self) -> ContentStatus:
        if self._content is None:
            return ContentStatus.PENDING_DOWNLOAD
        return ContentStatus.AVAILABLE
