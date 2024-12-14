from unittest.mock import MagicMock

import pytest

from licitpy.services.tender import TenderServices


@pytest.fixture
def mock_tender_services() -> TenderServices:
    return MagicMock(spec=TenderServices)
