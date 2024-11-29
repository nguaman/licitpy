from unittest.mock import Mock, patch

import pandas as pd
import pytest
from pydantic import HttpUrl

from licitpy.downloader.tender import TenderDownloader
from licitpy.parsers.tender import TenderParser
from licitpy.types.tender.status import StatusFromCSV
from licitpy.types.tender.tender import TenderFromCSV


@pytest.fixture
def tender_parser() -> TenderParser:
    """Fixture para proporcionar una instancia de TenderParser."""
    return TenderParser()


@pytest.fixture
def tender_downloader() -> TenderDownloader:
    return TenderDownloader()


def test_init_with_parser() -> None:
    mock_parser = Mock(spec=TenderParser)
    downloader = TenderDownloader(parser=mock_parser)

    assert downloader.parser == mock_parser


def test_init_without_parser() -> None:
    downloader = TenderDownloader()
    assert isinstance(downloader.parser, TenderParser)


def test_get_tender_from_csv(tender_downloader: TenderDownloader) -> None:
    mock_df = pd.DataFrame(
        {
            "CodigoExterno": ["1234-56-LQ20", "7890-12-LP21"],
            "FechaPublicacion": pd.to_datetime(["2024-11-01", "2024-11-02"]),
            "RegionUnidad": ["Región de Antofagasta ", "Región de Atacama "],
            "Estado": ["Adjudicada", "Publicada"],
            "Nombre": ["Título1", "Título2"],
            "Descripcion": ["Descripción1", "Descripción2"],
        }
    )

    with patch.object(
        tender_downloader, "get_massive_tenders_csv_from_zip", return_value=mock_df
    ):
        result = tender_downloader.get_tender_from_csv(2024, 11)

        expected = [
            TenderFromCSV(
                CodigoExterno="1234-56-LQ20",
                FechaPublicacion=pd.to_datetime("2024-11-01").date(),
                RegionUnidad="Región de Antofagasta",
                Estado=StatusFromCSV.AWARDED,
                Nombre="Título1",
                Descripcion="Descripción1",
            ),
            TenderFromCSV(
                CodigoExterno="7890-12-LP21",
                FechaPublicacion=pd.to_datetime("2024-11-02").date(),
                RegionUnidad="Región de Atacama",
                Estado=StatusFromCSV.PUBLISHED,
                Nombre="Título2",
                Descripcion="Descripción2",
            ),
        ]

        assert result == expected


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
