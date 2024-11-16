from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from licitpy.client.licitpy import Licitpy
from licitpy.entities.tenders import Tenders
from licitpy.types.search import TimeRange

TODAY = date(2024, 11, 15)
YESTERDAY = TODAY - timedelta(days=1)
START_DATE = "2024-11-01"
END_DATE = "2024-11-15"


@pytest.fixture
def licitpy_instance():
    """Fixture to provide a Licitpy instance with a mocked `get_monthly_tenders`."""
    licitpy = Licitpy()
    licitpy.licitpy.get_monthly_tenders = MagicMock(return_value=Tenders([]))
    return licitpy


def test_from_date_with_inverted_dates():
    """
    Test that `from_date` raises a ValueError if the start date is greater than the end date.
    """
    licitpy = Licitpy()
    with pytest.raises(ValueError, match="Start date cannot be greater than end date"):
        licitpy.from_date(start_date=END_DATE, end_date=START_DATE)


def test_from_date_with_explicit_dates(licitpy_instance):
    """
    Test that `from_date` processes explicit start and end dates correctly.
    """
    tenders = licitpy_instance.from_date(start_date=START_DATE, end_date=END_DATE)

    assert isinstance(
        tenders, Tenders
    ), "Expected `from_date` to return a Tenders object"
    licitpy_instance.licitpy.get_monthly_tenders.assert_called_once_with(
        date(2024, 11, 1), date(2024, 11, 15)
    )


def test_from_date_with_time_range_today(licitpy_instance):
    """
    Test that `from_date` handles the `TimeRange.TODAY` enum correctly.
    """
    with freeze_time(TODAY):
        tenders = licitpy_instance.from_date(time_range=TimeRange.TODAY)

        assert isinstance(
            tenders, Tenders
        ), "Expected `from_date` to return a Tenders object"
        licitpy_instance.licitpy.get_monthly_tenders.assert_called_once_with(
            TODAY, TODAY
        )


def test_from_date_with_time_range_this_month(licitpy_instance):
    """
    Test that `from_date` handles the `TimeRange.THIS_MONTH` enum correctly.
    """
    beginning_of_month = TODAY.replace(day=1)

    with freeze_time(TODAY):
        tenders = licitpy_instance.from_date(time_range=TimeRange.THIS_MONTH)

        assert isinstance(
            tenders, Tenders
        ), "Expected `from_date` to return a Tenders object"
        licitpy_instance.licitpy.get_monthly_tenders.assert_called_once_with(
            beginning_of_month, TODAY
        )


def test_from_date_with_time_range_from_yesterday(licitpy_instance):
    """
    Test that `from_date` handles the `TimeRange.FROM_YESTERDAY` enum correctly.
    """
    with freeze_time(TODAY):
        tenders = licitpy_instance.from_date(time_range=TimeRange.FROM_YESTERDAY)

        assert isinstance(
            tenders, Tenders
        ), "Expected `from_date` to return a Tenders object"
        licitpy_instance.licitpy.get_monthly_tenders.assert_called_once_with(
            YESTERDAY, YESTERDAY
        )
