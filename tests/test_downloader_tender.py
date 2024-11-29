from datetime import date
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest
from pydantic import HttpUrl

from licitpy.downloader.tender import TenderDownloader
from licitpy.parsers.tender import TenderParser
from licitpy.types.attachments import Attachment, FileType
from licitpy.types.tender.open_contract import (
    CompiledRelease,
    OpenContract,
    Period,
    Record,
    Tender,
)
from licitpy.types.tender.status import StatusFromCSV
from licitpy.types.tender.tender import (
    EnrichedTender,
    Region,
    TenderFromAPI,
    TenderFromCSV,
)


@pytest.fixture
def tender_downloader() -> TenderDownloader:
    return TenderDownloader()


@pytest.fixture
def mock_csv_data() -> pd.DataFrame:
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


def test_get_tender_from_csv(
    tender_downloader: TenderDownloader, mock_csv_data: pd.DataFrame
) -> None:
    with patch.object(
        tender_downloader,
        "get_massive_tenders_csv_from_zip",
        return_value=mock_csv_data,
    ):
        result = tender_downloader.get_tender_from_csv(2024, 11)

        expected = [
            TenderFromCSV(
                CodigoExterno="1234-56-LQ20",
                FechaPublicacion=date(2024, 11, 1),
                RegionUnidad="Región de Antofagasta",
                Estado=StatusFromCSV.AWARDED,
                Nombre="Título1",
                Descripcion="Descripción1",
            ),
            TenderFromCSV(
                CodigoExterno="7890-12-LP21",
                FechaPublicacion=date(2024, 11, 2),
                RegionUnidad="Región de Atacama",
                Estado=StatusFromCSV.PUBLISHED,
                Nombre="Título2",
                Descripcion="Descripción2",
            ),
        ]

        assert result == expected


def test_get_tender_codes_from_api(tender_downloader: TenderDownloader) -> None:
    mock_response = {
        "pagination": {"total": 2},
        "data": [
            {"urlTender": "https://example.com/1234-56-LQ20"},
            {"urlTender": "https://example.com/7890-12-LP21"},
        ],
    }

    with patch.object(
        tender_downloader.session, "get", return_value=Mock(json=lambda: mock_response)
    ):
        result = tender_downloader.get_tender_codes_from_api(2024, 11)

        expected = [
            TenderFromAPI(CodigoExterno="1234-56-LQ20"),
            TenderFromAPI(CodigoExterno="7890-12-LP21"),
        ]

        assert result == expected


def test_enrich_tender_with_ocds(tender_downloader: TenderDownloader) -> None:
    mock_data = OpenContract(
        uri="https://example.com",
        records=[
            Record(
                ocid="ocds-70d2nz-1234-56-LQ20",
                compiledRelease=CompiledRelease(
                    ocid="ocds-70d2nz-1234-56-LQ20",
                    tender=Tender(
                        id="1234-56-LQ20",
                        title="Test Title",
                        description="Test Description",
                        status="active",
                        tenderPeriod=Period(
                            startDate="2024-11-01T00:00:00Z",
                            endDate="2024-11-10T00:00:00Z",
                        ),
                    ),
                    parties=[
                        {
                            "name": "Entity Name",
                            "id": "CL-12345",
                            "roles": ["procuringEntity"],
                            "address": {
                                "streetAddress": "Street 123",
                                "region": "Región de Antofagasta ",
                                "countryName": "Chile",
                            },
                        }
                    ],
                ),
            )
        ],
    )

    with patch.object(
        tender_downloader, "get_tender_ocds_data_from_api", return_value=mock_data
    ):
        result = tender_downloader.enrich_tender_with_ocds("1234-56-LQ20")

        assert result.title == "Test Title"
        assert result.description == "Test Description"


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

        mock_head.assert_called_once_with(f"{base_url}?idlicitacion={code}")
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
        result = tender_downloader.get_tender_codes_from_api(2024, 11, limit=3)

        expected = [
            TenderFromAPI(CodigoExterno="1234-56-LQ20"),
            TenderFromAPI(CodigoExterno="7890-12-LP21"),
            TenderFromAPI(CodigoExterno="5678-90-LR22"),
        ]

        assert result == expected


def test_enrich_tender_with_ocds_invalid_data(
    tender_downloader: TenderDownloader,
) -> None:
    mock_data = OpenContract(uri="https://example.com", records=[])

    with patch.object(
        tender_downloader, "get_tender_ocds_data_from_api", return_value=mock_data
    ), pytest.raises(IndexError, match="list index out of range"):
        tender_downloader.enrich_tender_with_ocds("1234-56-LQ20")
