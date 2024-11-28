from datetime import date, timedelta
from typing import List

import pytest
from pytest_mock import MockerFixture

from licitpy.client.licitpy import Licitpy
from licitpy.entities.tender import Tender
from licitpy.sources.api import API
from licitpy.sources.local import Local
from licitpy.types.search import TimeRange
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Region


@pytest.fixture
def sample_tenders() -> List[Tender]:
    return [
        Tender(
            code="3955-54-LE24",
            region=Region.RM,
            status=Status.PUBLISHED,
            title="Tender 1",
            description="Description 1",
            opening_date=date(2024, 1, 1),
        ),
        Tender(
            code="4326-1-LR24",
            region=Region.V,
            status=Status.UNSUCCESSFUL,
            title="Tender 2",
            description="Description 2",
            opening_date=date(2024, 2, 1),
        ),
        Tender(
            code="750301-54-L124",
            region=Region.RM,
            status=Status.PUBLISHED,
            title="Tender 3",
            description="Description 3",
            opening_date=date(2024, 3, 1),
        ),
        Tender(
            code="2513-2-LE24",
            region=Region.V,
            status=Status.PUBLISHED,
            title="Tender 4",
            description="Description 4",
            opening_date=date(2024, 4, 1),
        ),
    ]


@pytest.fixture
def licitpy_local() -> Licitpy:
    return Licitpy()


@pytest.fixture
def licitpy_api() -> Licitpy:
    return Licitpy(api_key="licitpy-")


def test_licitpy_initialization_without_api_key(licitpy_local: Licitpy) -> None:
    assert isinstance(licitpy_local.licitpy, Local)


def test_licitpy_initialization_with_api_key(licitpy_api: Licitpy) -> None:
    assert isinstance(licitpy_api.licitpy, API)


def test_time_range_today() -> None:
    licitpy_instance = Licitpy()
    start_date, end_date = licitpy_instance._time_range(TimeRange.TODAY)
    assert start_date == date.today()
    assert end_date == date.today()


def test_time_range_from_yesterday() -> None:
    licitpy_instance = Licitpy()
    start_date, end_date = licitpy_instance._time_range(TimeRange.FROM_YESTERDAY)
    expected_date = date.today() - timedelta(days=1)
    assert start_date == expected_date
    assert end_date == expected_date


def test_time_range_this_month() -> None:
    licitpy_instance = Licitpy()
    start_date, end_date = licitpy_instance._time_range(TimeRange.THIS_MONTH)
    beginning_of_month = date.today().replace(day=1)
    assert start_date == beginning_of_month
    assert end_date == date.today()


def test_time_range_invalid() -> None:
    licitpy_instance = Licitpy()

    with pytest.raises(ValueError) as e:
        licitpy_instance._time_range(None)  # type: ignore

    assert "Unsupported time range" in str(e.value)


def test_date_range_with_dates() -> None:
    licitpy_instance = Licitpy()
    start = date(2024, 1, 1)
    end = date(2024, 1, 31)
    start_date, end_date = licitpy_instance._date_range(start, end)
    assert start_date == start
    assert end_date == end


def test_date_range_with_strings() -> None:
    licitpy_instance = Licitpy()
    start = "2024-01-01"
    end = "2024-01-31"
    start_date, end_date = licitpy_instance._date_range(start, end)
    assert start_date == date(2024, 1, 1)
    assert end_date == date(2024, 1, 31)


def test_date_range_with_time_range() -> None:
    licitpy_instance = Licitpy()
    start_date, end_date = licitpy_instance._date_range()
    beginning_of_month = date.today().replace(day=1)
    assert start_date == beginning_of_month
    assert end_date == date.today()


def test_from_date_invalid_date_range() -> None:
    licitpy_instance = Licitpy()
    with pytest.raises(ValueError) as e:
        licitpy_instance.from_date(
            start_date=date(2024, 2, 1), end_date=date(2024, 1, 1)
        )
    assert "Start date cannot be greater than end date" in str(e.value)


def test_from_code(mocker: MockerFixture, sample_tenders: List[Tender]) -> None:

    licitpy_instance = Licitpy()
    tender = sample_tenders[0]
    code = tender.code

    mock_get_tender = mocker.patch.object(
        licitpy_instance.licitpy, "get_tender", return_value=tender
    )

    result = licitpy_instance.from_code(code)

    assert result == tender

    mock_get_tender.assert_called_once_with(code)


def test_from_date_valid_dates(
    mocker: MockerFixture, sample_tenders: List[Tender]
) -> None:

    licitpy_instance = Licitpy()

    start_date = date(2024, 1, 1)
    end_date = date(2024, 4, 30)

    mock_get_monthly_tenders = mocker.patch.object(
        licitpy_instance.licitpy, "get_monthly_tenders", return_value=sample_tenders
    )

    result = licitpy_instance.from_date(start_date=start_date, end_date=end_date)

    assert result == sample_tenders

    mock_get_monthly_tenders.assert_called_once_with(start_date, end_date)
