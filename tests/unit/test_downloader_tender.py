from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest
from pydantic import HttpUrl
from pytest_mock import MockerFixture
from requests import Response

from licitpy.downloader.tender import TenderDownloader
from licitpy.types.tender.tender import TenderFromAPI


@pytest.fixture
def tender_downloader() -> TenderDownloader:
    """Returns a TenderDownloader instance"""
    return TenderDownloader()


@pytest.fixture
def mock_csv_data() -> pd.DataFrame:
    """Returns a mock DataFrame with tender data"""
    return pd.DataFrame(
        {
            "CodigoExterno": ["1234-56-LQ20", "7890-12-LP21"],
            "FechaPublicacion": pd.to_datetime(["2024-11-01", "2024-11-02"]),
            "RegionUnidad": ["Región de Antofagasta", "Región de Atacama"],
            "Estado": ["Adjudicada", "Publicada"],
            "Nombre": ["Título1", "Título2"],
            "Descripcion": ["Descripción1", "Descripción2"],
        }
    )


def test_get_tender_codes_from_api(
    tender_downloader: TenderDownloader, mocker: MockerFixture
) -> None:
    """Test the get_tender_codes_from_api method."""

    mock_response = {
        "pagination": {"total": 2},
        "data": [
            {"urlTender": "https://example.com/1234-56-LQ20"},
            {"urlTender": "https://example.com/7890-12-LP21"},
        ],
    }

    mock_get_response = MagicMock(spec=Response)
    mock_get_response.json.return_value = mock_response

    mocker.patch.object(
        tender_downloader.session,
        "get",
        return_value=mock_get_response,
    )

    result = tender_downloader.get_tenders_codes_from_api(2024, 11)

    assert result == [
        TenderFromAPI(code="1234-56-LQ20"),
        TenderFromAPI(code="7890-12-LP21"),
    ]


def test_get_tender_url_from_code(tender_downloader: TenderDownloader) -> None:
    code = "1234-56-LQ20"
    base_url = (
        "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"
    )
    expected_query = "abc123"
    expected_url = HttpUrl(f"{base_url}?qs={expected_query}")

    mock_response = Mock()
    mock_response.headers = {"Location": f"{base_url}?qs={expected_query}"}

    with patch.object(
        tender_downloader.session, "head", return_value=mock_response
    ) as mock_head:

        result = tender_downloader.get_tender_url_from_code(code)
        mock_head.assert_called_once_with(f"{base_url}?idlicitacion={code}", timeout=30)

        assert result == expected_url


def test_get_tender_codes_from_api_with_limit(
    tender_downloader: TenderDownloader,
) -> None:
    mock_response = {
        "pagination": {"total": 5},
        "data": [
            {"urlTender": "https://example.com/1234-56-LQ20"},
            {"urlTender": "https://example.com/7890-12-LP21"},
            {"urlTender": "https://example.com/5678-90-LR22"},
            {"urlTender": "https://example.com/3456-78-LR23"},
            {"urlTender": "https://example.com/9012-34-LP24"},
        ],
    }

    with patch.object(
        tender_downloader.session, "get", return_value=Mock(json=lambda: mock_response)
    ):
        result = tender_downloader.get_tenders_codes_from_api(2024, 11, limit=3)

        expected = [
            TenderFromAPI(code="1234-56-LQ20"),
            TenderFromAPI(code="7890-12-LP21"),
            TenderFromAPI(code="5678-90-LR22"),
        ]

        assert result == expected
