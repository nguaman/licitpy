from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

import pytest
from lxml.html import HtmlElement
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


def test_get_table_attachments(tender_parser: TenderParser) -> None:
    html = """
    <html>
        <body>
            <table id="DWNL_grdId">
                <tr><td>Sample Row</td></tr>
            </table>
        </body>
    </html>
    """
    table = tender_parser._get_table_attachments(html)
    assert table.tag == "table", "The tag of the returned element should be 'table'"


def test_get_table_attachments_not_found(tender_parser: TenderParser) -> None:
    html = "<html><body></body></html>"
    with pytest.raises(ValueError, match="Table with ID 'DWNL_grdId' not found"):
        tender_parser._get_table_attachments(html)


def test_get_table_attachments_rows(tender_parser: TenderParser) -> None:
    html = """
    <table>
        <tr class="row"><td>Row 1</td></tr>
        <tr class="row"><td>Row 2</td></tr>
    </table>
    """
    table = tender_parser.get_html_element(html)
    rows = tender_parser._get_table_attachments_rows(table)
    assert len(rows) == 2, "The number of rows should be 2"


def test_parse_size_attachment(tender_parser: TenderParser) -> None:
    html = "<td><span>1024 Kb</span></td>"
    element = tender_parser.get_html_element(html)
    size = tender_parser._parse_size_attachment(element)
    assert size == 1024 * 1024, "The parsed size should be 1 MB in bytes"


def test_extract_attachment_id(tender_parser: TenderParser) -> None:
    html = '<td><input id="ctl123" /></td>'
    element = tender_parser.get_html_element(html)
    attachment_id = tender_parser._extract_attachment_id(element)
    assert attachment_id == "123", "The extracted attachment ID should be '123'"


def test_extract_content_from_attachment_row(tender_parser: TenderParser) -> None:
    html = "<td><span>Attachment Content</span></td>"
    element = tender_parser.get_html_element(html)
    content = tender_parser._extract_content_from_attachment_row(element)
    assert content == "Attachment Content", "The extracted content should match"


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


def test_get_table_attachments_rows_valid(tender_parser: TenderParser) -> None:
    html = """
    <table>
        <tr class="row1"><td>Row 1</td></tr>
        <tr class="row2"><td>Row 2</td></tr>
        <tr class="row3"><td>Row 3</td></tr>
    </table>
    """
    table: HtmlElement = tender_parser.get_html_element(html)

    # Call the function
    rows = tender_parser._get_table_attachments_rows(table)

    # Assert that the correct number of rows is returned
    assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"

    # Optionally, validate the content of rows
    row_texts = [row.xpath("td/text()")[0] for row in rows]
    expected_texts = ["Row 1", "Row 2", "Row 3"]

    assert row_texts == expected_texts, f"Expected {expected_texts}, got {row_texts}"


def test_get_table_attachments_rows_no_rows(tender_parser: TenderParser) -> None:
    html = """
    <table>
        <!-- No rows with a class -->
    </table>
    """
    table: HtmlElement = tender_parser.get_html_element(html)

    # Call the function and expect an exception
    with pytest.raises(ValueError, match="No rows found in the table"):
        tender_parser._get_table_attachments_rows(table)


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


def test_parse_size_attachment_success(tender_parser: TenderParser) -> None:
    """
    Test that `_parse_size_attachment` correctly parses valid size values.
    """
    html = "<td><span>1024 Kb</span></td>"
    td_element = tender_parser.get_html_element(html)
    result = tender_parser._parse_size_attachment(td_element)
    expected_size = 1024 * 1024  # 1 MB in bytes
    assert result == expected_size, f"Expected {expected_size}, got {result}"


def test_parse_size_attachment_invalid_format(tender_parser: TenderParser) -> None:
    """
    Test that `_parse_size_attachment` raises a ValueError for invalid size formats.
    """
    html = "<td><span>invalid_size</span></td>"
    td_element = tender_parser.get_html_element(html)
    with pytest.raises(ValueError, match="Invalid size format: invalid_size"):
        tender_parser._parse_size_attachment(td_element)


def test_parse_size_attachment_missing_size(tender_parser: TenderParser) -> None:
    """
    Test that `_parse_size_attachment` raises an IndexError when size text is missing.
    """
    html = "<td></td>"
    td_element = tender_parser.get_html_element(html)
    with pytest.raises(IndexError, match="list index out of range"):
        tender_parser._parse_size_attachment(td_element)


def test_extract_attachment_id_no_input_id(tender_parser: TenderParser) -> None:
    """
    Test that `_extract_attachment_id` raises a ValueError when no input ID is found.
    """
    html = "<td></td>"  # No input element present
    td_element = tender_parser.get_html_element(html)

    with pytest.raises(ValueError, match="No input ID found in the first column"):
        tender_parser._extract_attachment_id(td_element)
