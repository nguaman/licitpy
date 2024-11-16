from datetime import date
from unittest.mock import MagicMock

import pytest

from licitpy.entities.tenders import Tenders
from licitpy.services.tender import TenderServices
from licitpy.sources.local import Local


def mock_service_get_tender_codes(year, month):
    """Mocked method to return tender codes for a given year and month."""
    return [
        {
            "CodigoExterno": f"{year}-{month}-T001",
            "FechaPublicacion": date(year, month, 1),
        },
        {
            "CodigoExterno": f"{year}-{month}-T002",
            "FechaPublicacion": date(year, month, 15),
        },
    ]


@pytest.fixture
def local_with_mocked_service():
    """Fixture to provide a Local instance with a mocked TenderServices."""
    service = TenderServices()
    service.get_tender_codes = MagicMock(side_effect=mock_service_get_tender_codes)
    return Local(service=service)


def test_get_monthly_tenders_single_month(local_with_mocked_service):
    """
    Test that get_monthly_tenders returns correct data for a single month.
    """
    start_date = date(2024, 11, 1)
    end_date = date(2024, 11, 30)

    tenders = local_with_mocked_service.get_monthly_tenders(
        start_date=start_date, end_date=end_date
    )

    # Validations
    assert isinstance(tenders, Tenders), "Expected result to be an instance of Tenders"
    assert tenders.count() == 2, "Expected two tenders to be returned"
    assert tenders.codes == ["2024-11-T002", "2024-11-T001"], "Tender codes mismatch"
