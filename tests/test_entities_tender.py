from datetime import datetime
from unittest.mock import MagicMock

import pytest

from licitpy.entities.tender import Tender
from licitpy.services.tender import TenderServices
from licitpy.types import Status


@pytest.fixture
def mock_tender_services():
    """Fixture to provide a mocked TenderServices instance."""
    services = MagicMock(spec=TenderServices)
    services.get_html.return_value = "<html>HTML</html>"
    services.get_status.return_value = Status.PUBLISHED
    services.get_url.return_value = "http://licitpy.dev/"
    services.get_title.return_value = "Title"
    services.get_opening_date.return_value = datetime(2024, 11, 15, 10, 0, 0)
    services.get_tier.return_value = "L1"
    return services


def test_tender_create_method():
    """Test that the Tender.create method creates a valid Tender instance."""
    tender = Tender.create("T001")

    assert tender.code == "T001", "Expected tender code to match 'T001'"
    assert isinstance(tender, Tender), "Expected instance to be of type Tender"


def test_tender_html_property(mock_tender_services):
    """Test that the html property retrieves HTML from TenderServices."""
    tender = Tender(code="T001", services=mock_tender_services)

    assert (
        tender.html == "<html>HTML</html>"
    ), "Expected HTML content to match the mocked return value"
    mock_tender_services.get_html.assert_called_once_with("http://licitpy.dev/")


def test_tender_url_property(mock_tender_services):
    """Test that the url property retrieves the correct URL from TenderServices."""
    tender = Tender(code="T001", services=mock_tender_services)

    assert (
        tender.url == "http://licitpy.dev/"
    ), "Expected URL to match the mocked return value"
    mock_tender_services.get_url.assert_called_once_with("T001")


def test_tender_tier_property(mock_tender_services):
    """Test that the tier property retrieves the correct tier from TenderServices."""
    tender = Tender(code="T001", services=mock_tender_services)

    assert tender.tier == "L1", "Expected tier to match the mocked return value"
    mock_tender_services.get_tier.assert_called_once_with("T001")
