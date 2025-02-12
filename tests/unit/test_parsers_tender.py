from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

import pytest
from pydantic import HttpUrl

from licitpy.parsers.base import ElementNotFoundException
from licitpy.parsers.tender import TenderParser
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import StatusFromImage, StatusFromOpenContract
from licitpy.types.tender.tender import Item, Region, Tier, Unit


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
    Test that `get_tender_status_from_html` correctly parses the status from the image source.
    """
    result = tender_parser.get_tender_status_from_html(example_html_status)
    expected_status = StatusFromImage.UNSUCCESSFUL
    assert result == expected_status, f"Expected {expected_status}, got {result}"


def test_get_tender_status_from_html_no_image(
    tender_parser: TenderParser, example_html_no_status_image: str
) -> None:
    """
    Test that `get_tender_status_from_html` raises an ElementNotFoundException when the image is not found.
    """
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'imgEstado' not found"
    ):
        tender_parser.get_tender_status_from_html(example_html_no_status_image)


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


def test_get_attachment_url_from_html(tender_parser: TenderParser) -> None:
    html = """
    <html>
        <body>
            <img id="imgAdjuntos" onclick="ViewAttachment.aspx?enc=testHash','"></img>
        </body>
    </html>
    """
    url = tender_parser.get_attachment_url_from_html(html)
    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/Procurement/Modules/Attachment/ViewAttachment.aspx?enc=testHash"
    )
    assert url == expected_url, f"The URL should be {expected_url}"


def test_get_purchase_orders_codes_from_html(tender_parser: TenderParser) -> None:
    html = """
    <html>
        <body>
            <a id="rptSearchOCDetail_ctl00_lkNumOC">750301-261-SE24</a>
            <a id="rptSearchOCDetail_ctl01_lkNumOC">750301-262-SE24</a>
            <a id="rptSearchOCDetail_ctl02_lkNumOC">750301-263-SE24</a>
        </body>
    </html>
    """

    # Run the function
    result = tender_parser.get_purchase_orders_codes_from_html(html)

    # Expected output
    expected_codes = ["750301-261-SE24", "750301-262-SE24", "750301-263-SE24"]

    # Assert the result matches the expected codes
    assert result == expected_codes, f"Expected {expected_codes}, got {result}"


def test_get_tender_purchase_order_url(tender_parser: TenderParser) -> None:
    html = """
    <html>
        <body>
            <a id="imgOrdenCompra" href="PopUpListOC.aspx?qs=testQueryString"></a>
        </body>
    </html>
    """

    # Run the function
    url = tender_parser.get_tender_purchase_order_url(html)

    # Expected URL
    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/Procurement/Modules/RFB/PopUpListOC.aspx?qs=testQueryString"
    )

    # Assert the result matches the expected URL
    assert url == expected_url, f"The URL should be {expected_url}"


def test_get_tender_purchase_order_url_no_query_string(
    tender_parser: TenderParser,
) -> None:
    html = """
    <html>
        <body>
            <a id="imgOrdenCompra" href="PopUpListOC.aspx"></a>
        </body>
    </html>
    """
    with pytest.raises(ValueError, match="Purchase Order query string not found"):
        tender_parser.get_tender_purchase_order_url(html)


@pytest.fixture
def html_items_sample() -> str:
    return """
        <div id="grvProducto_ctl02_lblNumero">1</div>
        <div id="grvProducto_ctl02_lblProducto">Tubos de ensayo multipropósito o generales</div>
        <div id="grvProducto_ctl02_lblCategoria">41121701</div>
        <div id="grvProducto_ctl02_lblDescripcion">PLUS HEMO LILA EDTA 3 ML</div>
        <div id="grvProducto_ctl02_lblCantidad">445000</div>
        <div id="grvProducto_ctl02_lblUnidad">Tubo</div>
    """


def test_get_item_from_code_success(
    tender_parser: TenderParser, html_items_sample: str
) -> None:
    result = tender_parser.get_item_from_code(html_items_sample, "02")

    expected_item = Item(
        index=1,
        title="Tubos de ensayo multipropósito o generales",
        category=41121701,
        description="PLUS HEMO LILA EDTA 3 ML",
        quantity=445000,
        unit=Unit.TUBE,
    )

    assert result == expected_item, f"Expected {expected_item}, got {result}"


def test_get_item_from_code_invalid_code(
    tender_parser: TenderParser, html_items_sample: str
) -> None:

    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'grvProducto_ctl99_lblNumero' not found",
    ):
        tender_parser.get_item_from_code(html_items_sample, "99")


def test_get_item_from_code_partial_data(
    tender_parser: TenderParser, html_items_sample: str
) -> None:

    # Remove the "Cantidad" field dynamically from the fixture
    incomplete_html = html_items_sample.replace(
        '<div id="grvProducto_ctl02_lblCantidad">445000</div>', ""
    )

    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'grvProducto_ctl02_lblCantidad' not found",
    ):
        tender_parser.get_item_from_code(incomplete_html, "02")


def test_get_item_codes_from_html_success(tender_parser: TenderParser) -> None:

    html = """
    <html>
        <div id="grvProducto_ctl02_lblNumero"></div>
        <div id="grvProducto_ctl03_lblNumero"></div>
        <div id="grvProducto_ctl04_lblNumero"></div>
        <div id="grvProducto_ctl05_lblNumero"></div>
        <div id="grvProducto_ctl06_lblNumero"></div>
        <div id="grvProducto_ctl07_lblNumero"></div>
        <div id="grvProducto_ctl08_lblNumero"></div>
    </html>
    """
    result = tender_parser.get_item_codes_from_html(html)
    expected_codes = ["02", "03", "04", "05", "06", "07", "08"]

    assert result == expected_codes, f"Expected {expected_codes}, got {result}"


def test_get_item_codes_from_html_no_matches(tender_parser: TenderParser) -> None:
    """
    Test that `get_item_codes_from_html` returns an empty list when no matches are found.
    """
    html = """
    <html>
        <div id="grvProducto_lblNumero"></div>
        <div id="grvProducto_ctl_lblNumero"></div>
    </html>
    """
    result = tender_parser.get_item_codes_from_html(html)
    expected_codes: List[str] = []

    assert result == expected_codes, f"Expected {expected_codes}, got {result}"


def test_get_closing_date_from_eligibility_valid_date(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_eligibility` correctly parses a valid closing date from the HTML.
    """
    html = """
    <html>
        <span id="lblFicha3CierreIdoneidad">16-12-2024 12:00:00</span>
    </html>
    """
    result = tender_parser.get_closing_date_from_eligibility(html)
    expected_date = datetime(
        2024, 12, 16, 12, 0, 0, tzinfo=ZoneInfo("America/Santiago")
    )
    assert result == expected_date, f"Expected {expected_date}, got {result}"


def test_get_closing_date_from_eligibility_missing_element(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_eligibility` raises an ElementNotFoundException
    when the element ID is not found in the HTML.
    """
    html = """
    <html>
        <span id="lblIncorrecto">16-12-2024 12:00:00</span>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'lblFicha3CierreIdoneidad' not found",
    ):
        tender_parser.get_closing_date_from_eligibility(html)


def test_get_closing_date_from_eligibility_invalid_date_format(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_eligibility` raises a ValueError
    when the extracted date has an invalid format.
    """
    html = """
    <html>
        <span id="lblFicha3CierreIdoneidad">16/12/2024 12:00:00</span>
    </html>
    """
    with pytest.raises(
        ValueError, match="time data '16/12/2024 12:00:00' does not match format"
    ):
        tender_parser.get_closing_date_from_eligibility(html)


def test_get_closing_date_from_eligibility_empty_date(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_eligibility` raises a ValueError
    when the extracted date is empty.
    """
    html = """
    <html>
        <span id="lblFicha3CierreIdoneidad"></span>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'lblFicha3CierreIdoneidad' has no attribute",
    ):
        tender_parser.get_closing_date_from_eligibility(html)


def test_get_closing_date_from_eligibility_timezone_conversion(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_eligibility` correctly applies the time zone to the parsed date.
    """
    html = """
    <html>
        <span id="lblFicha3CierreIdoneidad">16-12-2024 12:00:00</span>
    </html>
    """
    result = tender_parser.get_closing_date_from_eligibility(html)

    assert result.tzinfo == ZoneInfo(
        "America/Santiago"
    ), "The timezone should be America/Santiago"


def test_get_closing_date_from_html_eligibility_date(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_html` returns the date from lblFicha3CierreIdoneidad
    when it exists in the HTML.
    """
    html = """
    <html>
        <span id="lblFicha3CierreIdoneidad">16-12-2024 12:00:00</span>
    </html>
    """
    result = tender_parser.get_closing_date_from_html(html)
    expected_date = datetime(
        2024, 12, 16, 12, 0, 0, tzinfo=ZoneInfo("America/Santiago")
    )
    assert result == expected_date, f"Expected {expected_date}, got {result}"


def test_get_closing_date_from_html_closing_date(tender_parser: TenderParser) -> None:
    """
    Test that `get_closing_date_from_html` returns the date from lblFicha3Cierre
    when lblFicha3CierreIdoneidad does not exist.
    """
    html = """
    <html>
        <span id="lblFicha3Cierre">11-11-2024 15:00:00</span>
    </html>
    """
    result = tender_parser.get_closing_date_from_html(html)
    expected_date = datetime(
        2024, 11, 11, 15, 0, 0, tzinfo=ZoneInfo("America/Santiago")
    )
    assert result == expected_date, f"Expected {expected_date}, got {result}"


def test_get_closing_date_from_html_invalid_closing_date(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_html` raises a ValueError when lblFicha3Cierre
    contains an invalid date format.
    """
    html = """
    <html>
        <span id="lblFicha3Cierre">11/11/2024 15:00:00</span>
    </html>
    """
    with pytest.raises(
        ValueError, match="time data '11/11/2024 15:00:00' does not match format"
    ):
        tender_parser.get_closing_date_from_html(html)


def test_get_closing_date_from_html_missing_both_elements(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_closing_date_from_html` raises an ElementNotFoundException
    when both lblFicha3CierreIdoneidad and lblFicha3Cierre are missing.
    """
    html = """
    <html>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'lblFicha3Cierre' not found"
    ):
        tender_parser.get_closing_date_from_html(html)


def test_get_closing_date_from_html_timezone(tender_parser: TenderParser) -> None:
    """
    Test that `get_closing_date_from_html` applies the correct timezone (America/Santiago).
    """
    html = """
    <html>
        <span id="lblFicha3Cierre">11-11-2024 15:00:00</span>
    </html>
    """
    result = tender_parser.get_closing_date_from_html(html)
    assert result.tzinfo == ZoneInfo(
        "America/Santiago"
    ), "The timezone should be America/Santiago"


def test_get_closing_date_from_tender_ocds_data_end_date_none(
    tender_parser: TenderParser, example_open_contract: OpenContract
) -> None:
    """
    Test that `get_closing_date_from_tender_ocds_data` returns None when `endDate` is None.
    """
    example_open_contract.records[0].compiledRelease.tender.tenderPeriod.endDate = None

    result = tender_parser.get_closing_date_from_tender_ocds_data(example_open_contract)

    assert result is None, "Expected None when `endDate` is None"


def test_get_attachment_url_from_html_no_match(tender_parser: TenderParser) -> None:
    """
    Test that `get_attachment_url_from_html` raises a ValueError when the onclick attribute does not contain a valid URL.
    """
    html = """
    <html>
        <body>
            <img id="imgAdjuntos" onclick="InvalidClickHandler();" />
        </body>
    </html>
    """
    with pytest.raises(ValueError, match="Attachment URL hash not found"):
        tender_parser.get_attachment_url_from_html(html)


def test_get_attachment_url_from_html_missing_onclick(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_attachment_url_from_html` raises an ElementNotFoundException when the onclick attribute is missing.
    """
    html = """
    <html>
        <body>
            <img id="imgAdjuntos" />
        </body>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'imgAdjuntos' has no attribute '@onclick'",
    ):
        tender_parser.get_attachment_url_from_html(html)


def test_get_attachment_url_from_html_invalid_format(
    tender_parser: TenderParser,
) -> None:
    """
    Test that `get_attachment_url_from_html` raises a ValueError when the onclick attribute has an invalid format.
    """
    html = """
    <html>
        <body>
            <img id="imgAdjuntos" onclick="ViewAttachment.aspx?invalid" />
        </body>
    </html>
    """
    with pytest.raises(ValueError, match="Attachment URL hash not found"):
        tender_parser.get_attachment_url_from_html(html)


def test_get_tender_purchase_order_url_no_href(tender_parser: TenderParser) -> None:
    """
    Test that `get_tender_purchase_order_url` raises an ElementNotFoundException when the href attribute is missing.
    """
    html = """
    <html>
        <body>
            <a id="imgOrdenCompra"></a> <!-- Missing href attribute -->
        </body>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'imgOrdenCompra' has no attribute '@href'",
    ):
        tender_parser.get_tender_purchase_order_url(html)


def test_get_tender_purchase_order_url_empty_href(tender_parser: TenderParser) -> None:
    """
    Test that `get_tender_purchase_order_url` raises a ValueError when the href attribute is empty.
    """
    html = """
    <html>
        <body>
            <a id="imgOrdenCompra" href=""></a> <!-- Empty href attribute -->
        </body>
    </html>
    """
    with pytest.raises(ValueError, match="Purchase orders not found"):
        tender_parser.get_tender_purchase_order_url(html)


def test_get_questions_url_valid(tender_parser: TenderParser) -> None:
    """
    Test that `get_questions_url` correctly constructs a valid URL when the href contains a valid query string.
    """
    html = """
    <html>
        <body>
            <a id="imgPreguntasLicitacion" href="PopUps/PublicView.aspx?qs=testQueryString"></a>
        </body>
    </html>
    """
    result = tender_parser.get_questions_url(html)
    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/Foros/Modules/FNormal/PopUps/PublicView.aspx?qs=testQueryString"
    )
    assert result == expected_url, f"Expected {expected_url}, got {result}"


def test_get_questions_url_no_href(tender_parser: TenderParser) -> None:
    """
    Test that `get_questions_url` raises an ElementNotFoundException when the href attribute is missing.
    """
    html = """
    <html>
        <body>
            <a id="imgPreguntasLicitacion"></a> <!-- Missing href attribute -->
        </body>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'imgPreguntasLicitacion' has no attribute '@href'",
    ):
        tender_parser.get_questions_url(html)


def test_get_questions_url_missing_element(tender_parser: TenderParser) -> None:
    """
    Test that `get_questions_url` raises an ElementNotFoundException when the element with ID imgPreguntasLicitacion is missing.
    """
    html = """
    <html>
        <body>
            <!-- No element with ID imgPreguntasLicitacion -->
        </body>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'imgPreguntasLicitacion' not found",
    ):
        tender_parser.get_questions_url(html)


def test_get_questions_url_invalid_query_string(tender_parser: TenderParser) -> None:
    """
    Test that `get_questions_url` raises a ValueError when the href does not contain a valid query string.
    """
    html = """
    <html>
        <body>
            <a id="imgPreguntasLicitacion" href="PopUps/PublicView.aspx"></a> <!-- Missing qs= in href -->
        </body>
    </html>
    """
    with pytest.raises(ValueError, match="Questions query string not found"):
        tender_parser.get_questions_url(html)


def test_get_question_code_valid(tender_parser: TenderParser) -> None:
    """
    Test that `get_question_code` correctly retrieves the value from a valid element.
    """
    html = """
    <html>
        <body>
            <input id="h_intRBFCode" value="123456" />
        </body>
    </html>
    """
    result = tender_parser.get_question_code(html)
    expected_code = "123456"
    assert result == expected_code, f"Expected '{expected_code}', got '{result}'"


def test_get_question_code_missing_element(tender_parser: TenderParser) -> None:
    """
    Test that `get_question_code` raises an ElementNotFoundException when the element with the ID h_intRBFCode is missing.
    """
    html = """
    <html>
        <body>
            <!-- No element with ID h_intRBFCode -->
        </body>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'h_intRBFCode' not found",
    ):
        tender_parser.get_question_code(html)


def test_get_question_code_missing_value_attribute(tender_parser: TenderParser) -> None:
    """
    Test that `get_question_code` raises an ElementNotFoundException when the element lacks the value attribute.
    """
    html = """
    <html>
        <body>
            <input id="h_intRBFCode" />
        </body>
    </html>
    """
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'h_intRBFCode' has no attribute '@value'",
    ):
        tender_parser.get_question_code(html)


def test_get_question_code_empty_value(tender_parser: TenderParser) -> None:
    """
    Test that `get_question_code` returns an empty string when the value attribute is empty.
    """
    html = """
    <html>
        <body>
            <input id="h_intRBFCode" value="" />
        </body>
    </html>
    """
    result = tender_parser.get_question_code(html)
    assert result == "", "Expected an empty string when the value attribute is empty"
