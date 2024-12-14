from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
import requests

from licitpy.parsers.tender import TenderParser
from licitpy.types.tender.open_contract import OpenContract


@pytest.fixture
def tender_parser() -> TenderParser:
    return TenderParser()


@pytest.fixture
def tender_url_awarded() -> str:
    return "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=kB7wNzIM1HVt0mPcG7xAGw=="


@pytest.fixture
def tender_api_ocds_url_awarded() -> str:
    return "https://apis.mercadopublico.cl/OCDS/data/record/750301-54-L124"


@pytest.fixture
def tender_url_with_eligibility_closing_date() -> str:
    return "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=hIVAaNlCbpkWnsfJa/72Tw=="


@pytest.mark.integration
def test_closing_date_from_html(
    tender_parser: TenderParser, tender_url_awarded: str
) -> None:
    """
    Test that the closing date can be extracted from the HTML.
    """

    response = requests.get(tender_url_awarded)

    assert (
        response.status_code == 200
    ), f"Expected status 200, got {response.status_code}"

    html_content = response.content.decode("utf-8")

    closing_date = tender_parser.get_closing_date_from_html(html_content)

    expected_closing_date = datetime(
        2024, 11, 11, 15, 0, 0, tzinfo=ZoneInfo("America/Santiago")
    )

    assert (
        closing_date == expected_closing_date
    ), f"Expected {expected_closing_date}, got {closing_date}"


@pytest.mark.integration
def test_closing_date_from_ocds(
    tender_parser: TenderParser, tender_api_ocds_url_awarded: str
) -> None:

    response = requests.get(tender_api_ocds_url_awarded).json()
    data = OpenContract(**response)

    closing_date = tender_parser.get_closing_date_from_tender_ocds_data(data)
    expected_closing_date = datetime(
        2024, 11, 11, 15, 0, 0, tzinfo=ZoneInfo("America/Santiago")
    )

    assert (
        closing_date == expected_closing_date
    ), f"Expected {expected_closing_date}, got {closing_date}"


@pytest.mark.integration
def test_closing_date_with_eligibility_closing_date(
    tender_parser: TenderParser, tender_url_with_eligibility_closing_date: str
) -> None:

    response = requests.get(tender_url_with_eligibility_closing_date)

    assert (
        response.status_code == 200
    ), f"Expected status 200, got {response.status_code}"

    html_content = response.content.decode("utf-8")

    closing_date = tender_parser.get_closing_date_from_eligibility(html_content)

    # 16-12-2024 12:00:00
    expected_closing_date = datetime(
        2024, 12, 16, 12, 0, 0, tzinfo=ZoneInfo("America/Santiago")
    )

    assert (
        closing_date == expected_closing_date
    ), f"Expected {expected_closing_date}, got {closing_date}"
