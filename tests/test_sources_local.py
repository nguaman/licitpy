import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import date

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.services.tender import TenderServices
from licitpy.sources.local import Local
from licitpy.types.tender.tender import TenderFromCSV


@pytest.fixture
def mock_tender_services() -> TenderServices:
    return MagicMock(spec=TenderServices)


@pytest.fixture
def local_source(mock_tender_services: TenderServices) -> Local:
    return Local(service=mock_tender_services)


def test_get_monthly_tenders_empty_result(
    local_source: Local, mock_tender_services: Mock
) -> None:
    start_date = date(2024, 4, 1)
    end_date = date(2024, 4, 30)

    mock_tender_services.get_tenders.return_value = []

    result = local_source.get_monthly_tenders(start_date, end_date)

    assert isinstance(result, Tenders)
    assert len(result._tenders) == 0


def test_get_tender(local_source: Local) -> None:
    tender_code = "12345-1-LP24"

    with patch.object(
        Tender, "create", return_value=Tender(code=tender_code)
    ) as mock_create:
        tender = local_source.get_tender(tender_code)

        assert isinstance(tender, Tender)
        assert tender.code == tender_code
        mock_create.assert_called_once_with(tender_code)


def test_get_monthly_tenders_with_tenders(
    local_source: Local, mock_tender_services: MagicMock
) -> None:

    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)

    tender = TenderFromCSV(
        CodigoExterno="12345-1-LP24",
        FechaPublicacion="2024-01-15",
        RegionUnidad="Región Metropolitana de Santiago",
        Estado="Adjudicada",
        Nombre="Tender 1",
        Descripcion="Descripción 1",
    )

    mock_tender_services.get_tenders.return_value = [tender]

    result = local_source.get_monthly_tenders(start_date, end_date)

    assert isinstance(result, Tenders)
    assert len(result._tenders) == 1
    assert result._tenders[0].code == "12345-1-LP24"
