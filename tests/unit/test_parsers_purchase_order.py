import re
from datetime import date
from unittest.mock import patch

import pytest
from pydantic import HttpUrl

from licitpy.parsers.purchase_order import PurchaseOrderParser
from licitpy.types.geography import Commune, GeographyChile
from licitpy.types.purchase_order import Status


@pytest.fixture
def purchase_order_parser() -> PurchaseOrderParser:
    return PurchaseOrderParser()


def test_get_url_from_code(purchase_order_parser: PurchaseOrderParser) -> None:
    """
    Test that the method get_url_from_code returns the expected url
    """

    code = "12345678"

    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=12345678"
    )

    result = purchase_order_parser.get_url_from_code(code)

    assert result == expected_url, f"Expected {expected_url}, got {result}"


def test_get_purchase_order_status(purchase_order_parser: PurchaseOrderParser) -> None:
    """
    Test that the method get_purchase_order_status returns the expected status
    """

    html = """
    <html>
        <body>
            <span id="lblStatusPOValue">Aceptada</span>
        </body>
    </html>
    """

    expected_status = Status("Aceptada")

    with patch.object(
        purchase_order_parser, "get_text_by_element_id", return_value="Aceptada"
    ):
        result = purchase_order_parser.get_purchase_order_status(html)

    assert result == expected_status, f"Expected {expected_status}, got {result}"


def test_get_purchase_order_title_from_html(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_title_from_html returns the expected title
    """

    html = """
    <html>
        <body>
            <span id="lblNamePOValue">Orden de Compra Ejemplo</span>
        </body>
    </html>
    """
    expected_title = "Orden de Compra Ejemplo"

    with patch.object(
        purchase_order_parser,
        "get_text_by_element_id",
        return_value="Orden de Compra Ejemplo",
    ):
        result = purchase_order_parser.get_purchase_order_title_from_html(html)

    assert result == expected_title, f"Expected {expected_title}, got {result}"


def test_get_purchase_order_issue_date_from_html(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_issue_date_from_html returns the expected issue date
    """

    html = """
    <html>
        <body>
            <span id="lblCreationDatePOValue">06-12-2024</span>
        </body>
    </html>
    """
    expected_issue_date = date(2024, 12, 6)

    with patch.object(
        purchase_order_parser, "get_text_by_element_id", return_value="06-12-2024"
    ):
        result = purchase_order_parser.get_purchase_order_issue_date_from_html(html)

    assert (
        result == expected_issue_date
    ), f"Expected {expected_issue_date}, got {result}"


def test_get_purchase_order_issue_date_from_html_invalid_date(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_issue_date_from_html raises a ValueError for an invalid date
    """

    html = """
    <html>
        <body>
            <span id="lblCreationDatePOValue">invalid-date</span>
        </body>
    </html>
    """

    with patch.object(
        purchase_order_parser, "get_text_by_element_id", return_value="invalid-date"
    ):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "The date string 'invalid-date' does not match ISO (YYYY-MM-DD) or dd-mm-yyyy formats."
            ),
        ):
            purchase_order_parser.get_purchase_order_issue_date_from_html(html)


def test_get_purchase_order_tender_code_from_html(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_tender_code_from_html returns the expected tender code
    """

    html = """
    <html>
        <body>
            <span id="lblProvenience">750301-54-L124</span>
        </body>
    </html>
    """
    expected_tender_code = "750301-54-L124"

    with patch.object(
        purchase_order_parser, "get_text_by_element_id", return_value="750301-54-L124"
    ):
        result = purchase_order_parser.get_purchase_order_tender_code_from_html(html)

    assert (
        result == expected_tender_code
    ), f"Expected {expected_tender_code}, got {result}"


def test_get_purchase_order_tender_code_from_html_no_element(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_tender_code_from_html returns None if the element does not exist
    """

    html = """
    <html>
        <body>
        </body>
    </html>
    """

    with patch.object(purchase_order_parser, "has_element_id", return_value=False):
        result = purchase_order_parser.get_purchase_order_tender_code_from_html(html)

    assert result is None, f"Expected None, got {result}"


def test_get_purchase_order_tender_code_from_html_element_exists(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_tender_code_from_html returns the expected tender code if the element exists
    """

    html = """
    <html>
        <body>
            <span id="lblProvenience">750301-54-L124</span>
        </body>
    </html>
    """
    expected_tender_code = "750301-54-L124"

    with patch.object(purchase_order_parser, "has_element_id", return_value=True):
        with patch.object(
            purchase_order_parser,
            "get_text_by_element_id",
            return_value="750301-54-L124",
        ):
            result = purchase_order_parser.get_purchase_order_tender_code_from_html(
                html
            )

    assert (
        result == expected_tender_code
    ), f"Expected {expected_tender_code}, got {result}"


def test_get_purchase_order_commune_from_html(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_commune_from_html returns the expected commune
    """
    html = """
    <html>
        <body>
            <span id="lblCommuneValuePF">Santiago</span>
        </body>
    </html>
    """
    expected_commune = Commune("Viña del Mar")

    with patch.object(
        purchase_order_parser, "get_text_by_element_id", return_value="Viña del Mar"
    ):
        result = purchase_order_parser.get_purchase_order_commune_from_html(html)

    assert result == expected_commune, f"Expected {expected_commune}, got {result}"


def test_get_purchase_order_region_from_html(
    purchase_order_parser: PurchaseOrderParser,
) -> None:
    """
    Test that the method get_purchase_order_region_from_html returns the expected region
    """
    commune = Commune("Santiago")

    expected_region = GeographyChile[commune].region
    result = purchase_order_parser.get_purchase_order_region_from_html(commune)

    assert result == expected_region, f"Expected {expected_region}, got {result}"
