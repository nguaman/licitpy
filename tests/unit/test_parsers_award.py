import re
from unittest.mock import patch

import pytest
from pydantic import HttpUrl

from licitpy.parsers.award import AwardParser
from licitpy.parsers.base import ElementNotFoundException
from licitpy.types.award import Method


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
