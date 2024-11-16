from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from licitpy.parsers.tender import TenderParser
from licitpy.types import Status, Tier


@pytest.fixture
def tender_parser():
    """Fixture to provide a TenderParser instance."""
    return TenderParser()


def test_get_tender_opening_date_from_tender_ocds_data(tender_parser):
    """
    Test that the opening date is correctly parsed from OCDS data.
    """
    data = {
        "records": [
            {
                "compiledRelease": {
                    "tender": {"tenderPeriod": {"startDate": "2024-11-06T11:40:34Z"}}
                }
            }
        ]
    }
    expected_date = datetime(
        2024, 11, 6, 11, 40, 34, tzinfo=ZoneInfo("America/Santiago")
    )
    result = tender_parser.get_tender_opening_date_from_tender_ocds_data(data)
    assert result == expected_date, f"Expected {expected_date}, got {result}"


@pytest.mark.parametrize(
    "data, expected_status",
    [
        (
            {"records": [{"compiledRelease": {"tender": {"status": "active"}}}]},
            Status("active"),
        ),
        (
            {"records": [{"compiledRelease": {"tender": {"status": "cancelled"}}}]},
            Status("cancelled"),
        ),
    ],
)
def test_get_tender_status_from_tender_ocds_data(tender_parser, data, expected_status):
    """
    Test that the tender status is correctly parsed from OCDS data.
    """
    result = tender_parser.get_tender_status_from_tender_ocds_data(data)
    assert result == expected_status, f"Expected {expected_status}, got {result}"


@pytest.mark.parametrize(
    "data, expected_title",
    [
        (
            {
                "records": [
                    {"compiledRelease": {"tender": {"title": "Bridge Construction"}}}
                ]
            },
            "Bridge Construction",
        ),
        (
            {
                "records": [
                    {"compiledRelease": {"tender": {"title": "Road Maintenance"}}}
                ]
            },
            "Road Maintenance",
        ),
    ],
)
def test_get_tender_title_from_tender_ocds_data(tender_parser, data, expected_title):
    """
    Test that the tender title is correctly parsed from OCDS data.
    """
    result = tender_parser.get_tender_title_from_tender_ocds_data(data)
    assert result == expected_title, f"Expected {expected_title}, got {result}"


def test_get_tender_tier(tender_parser):
    """
    Test that the tender tier is correctly extracted from the tender code.
    """
    code = "ABC-123-L1"
    expected_tier = Tier("L1")
    result = tender_parser.get_tender_tier(code)
    assert result == expected_tier, f"Expected {expected_tier}, got {result}"
