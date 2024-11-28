from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from licitpy.parsers.base import ElementNotFoundException
from licitpy.parsers.tender import TenderParser
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import StatusFromImage, StatusFromOpenContract
from licitpy.types.tender.tender import Region, Tier


@pytest.fixture
def tender_parser() -> TenderParser:
    return TenderParser()


@pytest.fixture
def example_open_contract() -> OpenContract:
    """
    Fixture to provide a sample OpenContract instance using real-world data from JSON.
    """

    return OpenContract(
        **{
            "uri": "https://apis.mercadopublico.cl/OCDS/data/record/3955-54-LE24",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_breakdown_extension/master/extension.json",
                "https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/master/extension.json",
                "https://gitlab.com/dncp-opendata/ocds_planning_items_extension/-/raw/master/extension.json",
                "https://chilecompracl.visualstudio.com/a6a3f587-5f23-42f6-9255-ac5852fae1e7/_apis/git/repositories/fb91c43b-011b-434b-901d-9d36ec50c586/items?path=%2Fextension.json&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=master&resolveLfs=true&%24format=octetStream&api-version=5.0",
            ],
            "publisher": {"name": "Dirección de Compras y Contratación Pública"},
            "license": "https://creativecommons.org/publicdomain/zero/1.0/",
            "publishedDate": "2024-10-14T10:08:27Z",
            "records": [
                {
                    "ocid": "ocds-70d2nz-3955-54-LE24",
                    "compiledRelease": {
                        "ocid": "ocds-70d2nz-3955-54-LE24",
                        "tender": {
                            "id": "3955-54-LE24",
                            "title": "TRANSPORTE PARA SALIDAS PEDAGÓGICAS  SEP 2024 ESCUELA RECAREDO VIGUERAS ARANEDA",
                            "description": "ADQUISICION DE SERVICIO DE TRASLADO PARA ESTUDIANTES EN SALIDAS PEGAGÓGICAS DURANTE EL MES DE OCTUBRE Y NOVIEMBRE PARA ALUMNOS DE LA ESCUELA RECAREDO VIGUERAS ARANEDA DE LA COMUNA DE SANTA JUANA SEGUN DETALLE EN OFICIOS N° 133/134/ 150/154 Y DEMAS ANTECEDENTES ADJUNTOS",
                            "status": "complete",
                            "tenderPeriod": {
                                "startDate": "2024-10-04T15:25:56Z",
                                "endDate": "2024-10-10T12:42:00Z",
                            },
                        },
                        "parties": [
                            {
                                "name": "I MUNICIPALIDAD DE SANTA JUANA | D.A.E.M.",
                                "id": "CL-MP-4875",
                                "roles": ["procuringEntity"],
                                "address": {
                                    "streetAddress": "Irarrazabal 135",
                                    "region": "Región del Biobío",
                                    "countryName": "Chile",
                                },
                            }
                        ],
                    },
                }
            ],
        }
    )


@pytest.fixture
def example_html_status() -> str:
    return """
    <html>
        <body>
            <img id="imgEstado" src="../../Includes/images/FichaLight/iconos_estados/desierta.png" style="border-width:0px;">
        </body>
    </html>
    """


@pytest.fixture
def example_html_no_status_image() -> str:
    return """
    <html>
        <body>
        </body>
    </html>
    """


def test_get_tender_status_from_image_desierta(
    tender_parser: TenderParser, example_html_status: str
) -> None:
    """
    Test that `get_tender_status_from_image` correctly parses the status from the image source.
    """
    result = tender_parser.get_tender_status_from_image(example_html_status)
    expected_status = StatusFromImage.UNSUCCESSFUL
    assert result == expected_status, f"Expected {expected_status}, got {result}"


def test_get_tender_status_from_image_no_image(
    tender_parser: TenderParser, example_html_no_status_image: str
) -> None:
    """
    Test that `get_tender_status_from_image` raises an ElementNotFoundException when the image is not found.
    """
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'imgEstado' not found"
    ):
        tender_parser.get_tender_status_from_image(example_html_no_status_image)


def test_get_tender_opening_date_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_opening_date_from_tender_ocds_data` correctly parses the opening date.
    """
    result = tender_parser.get_tender_opening_date_from_tender_ocds_data(
        example_open_contract
    )
    expected = datetime(2024, 10, 4, 15, 25, 56, tzinfo=ZoneInfo("America/Santiago"))

    assert result == expected, f"Expected {expected}, got {result}"


def test_get_closing_date_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_closing_date_from_tender_ocds_data` correctly parses the closing date.
    """
    result = tender_parser.get_closing_date_from_tender_ocds_data(example_open_contract)
    expected = datetime(2024, 10, 10, 12, 42, 0, tzinfo=ZoneInfo("America/Santiago"))

    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_status_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_status_from_tender_ocds_data` correctly parses the tender status.
    """
    result = tender_parser.get_tender_status_from_tender_ocds_data(
        example_open_contract
    )
    expected = StatusFromOpenContract.AWARDED
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_title_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_title_from_tender_ocds_data` correctly parses the tender title.
    """
    result = tender_parser.get_tender_title_from_tender_ocds_data(example_open_contract)
    expected = "TRANSPORTE PARA SALIDAS PEDAGÓGICAS  SEP 2024 ESCUELA RECAREDO VIGUERAS ARANEDA"

    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_description_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_description_from_tender_ocds_data` correctly parses the tender description.
    """
    result = tender_parser.get_tender_description_from_tender_ocds_data(
        example_open_contract
    )
    expected = "ADQUISICION DE SERVICIO DE TRASLADO PARA ESTUDIANTES EN SALIDAS PEGAGÓGICAS DURANTE EL MES DE OCTUBRE Y NOVIEMBRE PARA ALUMNOS DE LA ESCUELA RECAREDO VIGUERAS ARANEDA DE LA COMUNA DE SANTA JUANA SEGUN DETALLE EN OFICIOS N° 133/134/ 150/154 Y DEMAS ANTECEDENTES ADJUNTOS"

    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_region_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_region_from_tender_ocds_data` correctly parses the tender region.
    """
    result = tender_parser.get_tender_region_from_tender_ocds_data(
        example_open_contract
    )
    expected = Region.VIII

    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_tier(tender_parser: TenderParser) -> None:
    """
    Test that `get_tender_tier` correctly extracts the tier from the tender code.
    """
    result = tender_parser.get_tender_tier("3955-54-LE24")
    expected = Tier.LE
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_code_from_tender_ocds_data(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_code_from_tender_ocds_data` correctly extracts the tender code.
    """
    result = tender_parser.get_tender_code_from_tender_ocds_data(example_open_contract)
    expected = "3955-54-LE24"
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_tender_region_invalid_entity(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_region_from_tender_ocds_data` raises a ValueError when no procuring entity is found.
    """
    example_open_contract.records[0].compiledRelease.parties = []

    with pytest.raises(
        ValueError,
        match="There must be exactly one entity with the role of procuringEntity.",
    ):
        tender_parser.get_tender_region_from_tender_ocds_data(example_open_contract)


def test_get_tender_tier_invalid_code(tender_parser: TenderParser) -> None:
    """
    Test that `get_tender_tier` raises a ValueError for invalid tender codes.
    """
    invalid_code = "3955-54"

    with pytest.raises(ValueError):
        tender_parser.get_tender_tier(invalid_code)


def test_get_tender_region_missing_address(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_tender_region_from_tender_ocds_data` raises a ValueError
    when the address is missing for the procuring entity.
    """
    # Set the address to None
    example_open_contract.records[0].compiledRelease.parties[0].address = None

    with pytest.raises(
        ValueError, match="The address or region is missing for the procuring entity."
    ):
        tender_parser.get_tender_region_from_tender_ocds_data(example_open_contract)
