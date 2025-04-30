import re
from typing import List
from unittest.mock import patch

import pytest
from pydantic import HttpUrl

from licitpy.parsers.award import AwardParser
from licitpy.parsers.base import ElementNotFoundException
from licitpy.types.award import (
    AwardResult,
    ItemAward,
    ItemAwardStatus,
    Method,
    SupplierBid,
)


@pytest.fixture
def award_parser() -> AwardParser:
    return AwardParser()


def test_get_url_from_html_valid(award_parser: AwardParser) -> None:
    """
    Test that get_url_from_html returns the expected URL when the query string is present.
    """
    fake_href = (
        "/Procurement/Modules/RFB/StepsProcessAward/PreviewAwardAct.aspx?qs=abcdef"
    )

    # Patch the get_href_by_element_id method to return a fake href containing the query string.
    with patch.object(award_parser, "get_href_by_element_id", return_value=fake_href):
        result = award_parser.get_url_from_html("<html>")

    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/Procurement/Modules/RFB/StepsProcessAward/PreviewAwardAct.aspx?qs=abcdef"
    )

    assert result == expected_url, f"Expected {expected_url}, got {result}"


def test_get_url_from_html_invalid(award_parser: AwardParser) -> None:
    """
    Test that get_url_from_html raises a ValueError when the query string is not present.
    """
    fake_href = "https://example.com/image.png"

    # Patch the get_href_by_element_id method to return a fake href without a query string.
    with patch.object(award_parser, "get_href_by_element_id", return_value=fake_href):
        with pytest.raises(
            ValueError, match=re.escape("Awarded query string not found")
        ):
            award_parser.get_url_from_html("<html>")


def test_get_method_from_html_valid() -> None:
    """
    Test that get_method_from_html returns the expected Method when the element is present.
    """
    html = """
    <html>
      <body>
        <span id="lblAwardTypeShow">Adjudicación Múltiple sin Emisión de OC</span>
      </body>
    </html>
    """
    parser = AwardParser()

    result = parser.get_method_from_html(html)
    expected = Method("Adjudicación Múltiple sin Emisión de OC")

    assert result == expected, f"Expected {expected}, got {result}"


def test_get_method_from_html_missing_element() -> None:
    """
    Test that get_method_from_html raises ElementNotFoundException if the element is missing.
    """
    html = """
    <html>
      <body>
        <span id="someOtherElement">Some Value</span>
      </body>
    </html>
    """
    parser = AwardParser()
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'lblAwardTypeShow' not found"
    ):
        parser.get_method_from_html(html)


def test_get_award_amount_from_html_valid() -> None:
    """
    Test that an integer amount is correctly parsed from the HTML content.
    """
    html = """
    <html>
      <body>
        <span id="lblAmountShow">1.234.567</span>
      </body>
    </html>
    """
    parser = AwardParser()
    result = parser.get_award_amount_from_html(html)
    assert result == 1234567, f"Expected 1234567, got {result}"


def test_get_award_amount_from_html_missing_element() -> None:
    """
    Test that an ElementNotFoundException is raised when lblAmountShow is missing.
    """
    html = """
    <html>
      <body>
        <span id="someOtherElement">2.345.678</span>
      </body>
    </html>
    """
    parser = AwardParser()
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'lblAmountShow' not found"
    ):
        parser.get_award_amount_from_html(html)


def test_get_estimated_amount_from_html_valid() -> None:
    """
    Test that an integer estimated amount is correctly parsed from the HTML content.
    """
    html = """
    <html>
      <body>
        <span id="lblEstimatedAmountShow">5.678.910</span>
      </body>
    </html>
    """
    parser = AwardParser()
    result = parser.get_estimated_amount_from_html(html)
    assert result == 5678910, f"Expected 5678910, got {result}"


def test_get_estimated_amount_from_html_missing_element() -> None:
    """
    Test that an ElementNotFoundException is raised when lblEstimatedAmountShow is missing.
    """
    html = """
    <html>
      <body>
        <span id="someOtherElement">6.789.012</span>
      </body>
    </html>
    """
    parser = AwardParser()
    with pytest.raises(
        ElementNotFoundException,
        match="Element with ID 'lblEstimatedAmountShow' not found",
    ):
        parser.get_estimated_amount_from_html(html)


def test_get_codes_from_html_valid(award_parser: AwardParser) -> None:
    """
    Test that get_codes_from_html returns the expected list of codes when the elements are present.
    """
    html = """
    <html>
      <body>
        <span id="grdItemOC_ctl02_ucAward__lblNumber">Item 1</span>
        <span id="grdItemOC_ctl03_ucAward__lblNumber">Item 2</span>
        <span id="grdItemOC_ctl04_ucAward__lblNumber">Item 3</span>
      </body>
    </html>
    """
    result = award_parser.get_codes_from_html(html)
    expected = ["02", "03", "04"]
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_codes_from_html_no_codes(award_parser: AwardParser) -> None:
    """
    Test that get_codes_from_html returns an empty list when no elements are present.
    """
    html = """
    <html>
      <body>
        <span id="someOtherElement">No items</span>
      </body>
    </html>
    """
    result = award_parser.get_codes_from_html(html)

    expected: List[str] = []
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_total_of_items_valid(award_parser: AwardParser) -> None:
    """
    Test that get_total_of_items returns the correct number of items.
    """
    codes = ["02", "03", "04"]
    result = award_parser.get_total_of_items(codes)
    assert result == 3, f"Expected 3, got {result}"


def test_get_total_of_items_empty(award_parser: AwardParser) -> None:
    """
    Test that get_total_of_items returns 0 when the list is empty.
    """
    codes: List[str] = []
    result = award_parser.get_total_of_items(codes)
    assert result == 0, f"Expected 0, got {result}"


def test_get_suppliers_codes_from_item_valid(award_parser: AwardParser) -> None:
    """
    Test that get_suppliers_codes_from_item returns the expected list of supplier codes when the elements are present.
    """
    html = """
    <html>
      <body>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_lblOrganization">Supplier 1</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl03_gvLines_lblOrganization">Supplier 2</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl04_gvLines_lblOrganization">Supplier 3</span>
      </body>
    </html>
    """
    result = award_parser.get_suppliers_codes_from_item(html, "02")
    expected = ["02", "03", "04"]
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_suppliers_codes_from_item_no_codes(award_parser: AwardParser) -> None:
    """
    Test that get_suppliers_codes_from_item returns an empty list when no elements are present.
    """
    html = """
    <html>
      <body>
        <span id="someOtherElement">No suppliers</span>
      </body>
    </html>
    """
    result = award_parser.get_suppliers_codes_from_item(html, "02")
    expected: List[str] = []
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_results_from_html_valid(award_parser: AwardParser) -> None:
    """
    Test that get_results_from_html returns the expected AwardResult when the elements are present.
    """
    html = """
    <html>
      <body>
        <span id="grdItemOC_ctl02_ucAward__lblNumber">1</span>
        <span id="grdItemOC_ctl02_ucAward_lblCodeonu">ONU Code 1</span>
        <span id="grdItemOC_ctl02_ucAward__LblSchemaTittle">Item Name 1</span>
        <span id="grdItemOC_ctl02_ucAward_lblDescription">Item Description 1</span>
        <span id="grdItemOC_ctl02_ucAward__LblRBICuantityNumber">10</span>
        <span id="grdItemOC_ctl02_ucAward_lblTotalLine">1.000</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_lblOrganization">33.333.333-3 DISTRIBUIDORA LIMITADA</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_lblSupplierComment">Comment 1</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_lblTotalNetPrice">500</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_txtAwardedQuantity">5</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_lblTotalNetAward">500</span>
        <span id="grdItemOC_ctl02_ucAward_gvLines_ctl02_gvLines_lblIsSelected">No Adjudicada</span>
        <span id="lblAmountTotalDetail">1.000</span>
      </body>
    </html>
    """
    result = award_parser.get_results_from_html(html)
    expected = AwardResult(
        items=[
            ItemAward(
                item_index=1,
                item_onu="ONU Code 1",
                item_name="Item Name 1",
                item_description="Item Description 1",
                item_quantity="10",
                item_total_awarded_amount=1000,
                suppliers=[
                    SupplierBid(
                        supplier_name="DISTRIBUIDORA LIMITADA",
                        supplier_item_description="Comment 1",
                        supplier_bid_total_price="500",
                        supplier_awarded_quantity="5",
                        supplier_total_awarded_amount="500",
                        supplier_bid_result=ItemAwardStatus("No Adjudicada"),
                        supplier_rut="33.333.333-3",
                    )
                ],
            )
        ],
        total_awarded_amount=1000,
    )
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_results_from_html_missing_element(award_parser: AwardParser) -> None:
    """
    Test that get_results_from_html raises ElementNotFoundException if a required element is missing.
    """
    html = """
    <html>
      <body>
        <span id="someOtherElement">Some Value</span>
      </body>
    </html>
    """
    with pytest.raises(ElementNotFoundException):
        award_parser.get_results_from_html(html)
