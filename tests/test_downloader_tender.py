from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from licitpy.downloader.tender import TenderDownloader


@pytest.fixture
def downloader():
    """Fixture to provide a TenderDownloader instance."""
    return TenderDownloader()


def test_get_tender_codes_from_api_normal_case(downloader):
    """
    Test that `get_tender_codes_from_api` returns the correct tender codes
    in a normal scenario.
    """
    mock_response = MagicMock(
        json=lambda: {
            "pagination": {"total": 100},
            "data": [{"urlTender": "https://licitpy.dev/T001"}],
        }
    )
    downloader.session.get = MagicMock(return_value=mock_response)

    tenders = downloader.get_tender_codes_from_api(year=2024, month=11, limit=10)

    assert len(tenders) == 1, "Expected one tender code to be returned"
    assert tenders[0] == {"CodigoExterno": "T001"}, "Expected tender code to match"


@patch("licitpy.downloader.tender.zipfile.ZipFile")
@patch("licitpy.downloader.tender.base64.b64decode")
def test_get_massive_tenders_csv_from_zip(mock_b64decode, mock_zipfile, downloader):
    """
    Test that `get_massive_tenders_csv_from_zip` correctly processes a zip file
    containing tender data.
    """
    mock_b64decode.return_value = b"mock zip content"
    mock_zip = mock_zipfile.return_value
    mock_zip.namelist.return_value = ["file.csv"]
    mock_zip.open.return_value = MagicMock()

    with patch(
        "pandas.read_csv",
        return_value=pd.DataFrame(
            {
                "CodigoExterno": ["T001"],
                "FechaPublicacion": ["2024-11-01"],
                "RegionUnidad": ["Region"],
            }
        ),
    ):
        df = downloader.get_massive_tenders_csv_from_zip(year=2024, month=11)

    assert not df.empty, "Expected DataFrame to be non-empty"
    assert (
        "CodigoExterno" in df.columns
    ), "Expected DataFrame to contain 'CodigoExterno'"


@patch.object(TenderDownloader, "get_massive_tenders_csv_from_zip")
def test_get_tender_from_csv(mock_csv, downloader):
    """
    Test that `get_tender_from_csv` correctly retrieves tenders from CSV data.
    """
    mock_csv.return_value = pd.DataFrame(
        {
            "CodigoExterno": ["T001", "T002"],
            "FechaPublicacion": [
                pd.Timestamp("2024-11-01"),
                pd.Timestamp("2024-11-02"),
            ],
            "RegionUnidad": ["IV", "III"],
        }
    )

    tenders = downloader.get_tender_from_csv(year=2024, month=11, limit=1)

    assert len(tenders) == 1, "Expected one tender to be returned"
    assert (
        tenders[0]["CodigoExterno"] == "T001"
    ), "Expected first tender to match 'T001'"


def test_get_tender_ocds_data(downloader):
    """
    Test that `get_tender_ocds_data` correctly fetches OCDS data for a tender.
    """
    downloader.session.get = MagicMock(
        return_value=MagicMock(json=MagicMock(return_value={"records": []}))
    )

    data = downloader.get_tender_ocds_data("T001")

    assert data == {"records": []}, "Expected OCDS data to be an empty records list"
    downloader.session.get.assert_called(), "Expected session.get to be called"


def test_get_tender_codes(downloader):
    """
    Test that `get_tender_codes` aggregates tender codes correctly
    from different sources.
    """
    downloader.get_tender_codes_from_api = MagicMock(
        return_value=[{"CodigoExterno": "T003"}]
    )
    downloader.get_tender_from_csv = MagicMock(
        return_value=[
            {
                "CodigoExterno": "T001",
                "FechaPublicacion": datetime(2024, 11, 1).date(),
                "RegionUnidad": "Region III",
            },
            {
                "CodigoExterno": "T002",
                "FechaPublicacion": datetime(2024, 11, 15).date(),
                "RegionUnidad": "Region IV",
            },
        ]
    )
    downloader.get_tender_publish_date_from_tender = MagicMock(
        return_value=datetime(2024, 11, 20)
    )

    tenders = downloader.get_tender_codes(2024, 11)

    assert len(tenders) == 3, "Expected three tenders to be aggregated"
    assert (
        tenders[0]["CodigoExterno"] == "T001"
    ), "Expected first tender code to match 'T001'"
    assert (
        tenders[1]["CodigoExterno"] == "T002"
    ), "Expected second tender code to match 'T002'"
    assert (
        tenders[2]["CodigoExterno"] == "T003"
    ), "Expected third tender code to match 'T003'"
    assert (
        tenders[2]["FechaPublicacion"] == datetime(2024, 11, 20).date()
    ), "Expected third tender's publication date to match '2024-11-20'"
