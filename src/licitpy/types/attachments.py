from enum import Enum
from typing import Optional

from pydantic import BaseModel, PrivateAttr, computed_field


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
    _file_type: Optional[str] = None
    _download_fn: Optional[callable] = PrivateAttr()
    _content: Optional[str] = None

    @property
    def content(self) -> Optional[str]:
        self._file_type, self._content = self._download_fn()
        return self._content

    @property
    def file_type(self) -> str:
        if self._file_type is None:
            _ = self.content

        return self._file_type

    @computed_field(return_type=ContentStatus)
    @property
    def content_status(self) -> ContentStatus:
        """
        Indicates if the content has been downloaded.

        - `PENDING_DOWNLOAD`: Content is ready to be downloaded. Access `.content` to download.
        - `AVAILABLE`: Content has been downloaded and is ready to use.

        To trigger the download, access `.content`.
        """
        if self._content is None:
            return ContentStatus.PENDING_DOWNLOAD

        return ContentStatus.AVAILABLE
