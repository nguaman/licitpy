from unittest.mock import patch

import pytest
from pydantic import HttpUrl

from licitpy.parsers.purchase_order import PurchaseOrderParser
from licitpy.types.purchase_order import Status


@pytest.fixture
def purchase_order_parser() -> PurchaseOrderParser:
    return PurchaseOrderParser()


def test_get_url_from_code(purchase_order_parser: PurchaseOrderParser) -> None:
    code = "12345678"
    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=12345678"
    )

    result = purchase_order_parser.get_url_from_code(code)

    assert result == expected_url, f"Expected {expected_url}, got {result}"


def test_get_purchase_order_status(purchase_order_parser: PurchaseOrderParser) -> None:
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
