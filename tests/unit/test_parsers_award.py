import re
from unittest.mock import patch

import pytest
from pydantic import HttpUrl

from licitpy.parsers.award import AwardParser


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
