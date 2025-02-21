from datetime import date, datetime, timedelta
from typing import Union
from zoneinfo import ZoneInfo

import pytest

from licitpy.types.search import TimeRange
from licitpy.utils.date import (
    _time_range,
    convert_to_date,
    convert_to_datetime,
    determine_date_range,
)


@pytest.mark.parametrize(
    "date_value, expected_date",
    [
        ("2024-01-01", date(2024, 1, 1)),
        ("2023-12-31", date(2023, 12, 31)),
        (date(2024, 1, 1), date(2024, 1, 1)),
        (date(2023, 12, 31), date(2023, 12, 31)),
    ],
)
def test_convert_to_date(date_value: str | date, expected_date: date) -> None:
    """
    Test that `convert_to_date` correctly converts string and date inputs to date objects.
    """
    result = convert_to_date(date_value)
    assert result == expected_date, f"Expected {expected_date}, got {result}"


def test_convert_to_date_invalid_string() -> None:
    """
    Test that `convert_to_date` raises a ValueError for invalid date strings.
    """
    with pytest.raises(ValueError):
        convert_to_date("invalid-date")


def test_convert_to_date_none() -> None:
    """
    Test that `convert_to_date` raises a TypeError when None is passed.
    """
    with pytest.raises(TypeError):
        convert_to_date(None)  # type: ignore[arg-type]


def test_convert_to_date_empty_string() -> None:
    """
    Test that `convert_to_date` raises a ValueError for empty date strings.
    """
    with pytest.raises(ValueError):
        convert_to_date("")


def test_convert_to_date_unexpected_type() -> None:
    """
    Test that `convert_to_date` raises a TypeError for unexpected input types.
    """
    with pytest.raises(TypeError):
        convert_to_date(12345)  # type: ignore[arg-type]


def test_convert_to_datetime_valid_date() -> None:
    """
    Test that `convert_to_datetime` correctly converts a valid date string.
    """

    date_str = "14-12-2024 15:30:00"
    input_format = "%d-%m-%Y %H:%M:%S"

    expected_datetime = datetime(
        2024, 12, 14, 15, 30, 0, tzinfo=ZoneInfo("America/Santiago")
    )
    result = convert_to_datetime(date_str, input_format)

    assert result == expected_datetime, f"Expected {expected_datetime}, got {result}"


def test_convert_to_datetime_invalid_format() -> None:
    """
    Test that `convert_to_datetime` raises a ValueError for an invalid date format.
    """
    date_str = "14-12-2024 15:30:00"
    input_format = "%Y-%m-%d %H:%M:%S"

    with pytest.raises(
        ValueError,
        match="Invalid date format: 14-12-2024 15:30:00. Expected format: '%Y-%m-%d %H:%M:%S'",
    ):
        convert_to_datetime(date_str, input_format)


def test_convert_to_datetime_none() -> None:
    """
    Test that `convert_to_datetime` raises a TypeError when None is passed.
    """
    with pytest.raises(TypeError):
        convert_to_datetime(None, "%d-%m-%Y %H:%M:%S")  # type: ignore[arg-type]


def test_convert_to_datetime_empty_string() -> None:
    """
    Test that `convert_to_datetime` raises a ValueError for empty date strings.
    """
    with pytest.raises(ValueError):
        convert_to_datetime("", "%d-%m-%Y %H:%M:%S")


def test_convert_to_datetime_unexpected_type() -> None:
    """
    Test that `convert_to_datetime` raises a TypeError for unexpected input types.
    """
    with pytest.raises(TypeError):
        convert_to_datetime(12345, "%d-%m-%Y %H:%M:%S")  # type: ignore[arg-type]


def test_time_range_today() -> None:
    """
    Test that `_time_range` returns the correct date range for TimeRange.TODAY.
    """

    today = date.today()
    expected_range = (today, today)
    result = _time_range(TimeRange.TODAY)

    assert result == expected_range, f"Expected {expected_range}, got {result}"


def test_time_range_from_yesterday() -> None:
    """
    Test that `_time_range` returns the correct date range for TimeRange.FROM_YESTERDAY.
    """

    today = date.today()
    yesterday = today - timedelta(days=1)
    expected_range = (yesterday, yesterday)
    result = _time_range(TimeRange.FROM_YESTERDAY)

    assert result == expected_range, f"Expected {expected_range}, got {result}"


def test_time_range_this_month() -> None:
    """
    Test that `_time_range` returns the beginning of the month and today's date for TimeRange.THIS_MONTH.
    """

    today = date.today()
    beginning_of_month = today.replace(day=1)
    start_date, end_date = _time_range(TimeRange.THIS_MONTH)

    assert (
        start_date == beginning_of_month
    ), f"Expected {beginning_of_month}, got {start_date}"

    assert end_date == today, f"Expected {today}, got {end_date}"


def test_time_range_invalid() -> None:
    """
    Test that `_time_range` raises a ValueError for an invalid TimeRange.
    """
    with pytest.raises(ValueError):
        _time_range("INVALID")  # type: ignore[arg-type]


def test_determine_date_range_no_dates() -> None:
    """
    Test that `determine_date_range` returns the correct range when no dates are provided.
    """

    expected_start, expected_end = date.today().replace(day=1), date.today()
    result_start, result_end = determine_date_range()

    assert (
        result_start == expected_start
    ), f"Expected start date {expected_start}, got {result_start}"

    assert (
        result_end == expected_end
    ), f"Expected end date {expected_end}, got {result_end}"


def test_determine_date_range_valid_time_range() -> None:
    """
    Test that `determine_date_range` correctly returns a range for a valid TimeRange.
    """
    time_range = TimeRange.TODAY
    expected_range = _time_range(time_range)

    result = determine_date_range(time_range=time_range)

    assert result == expected_range, f"Expected {expected_range}, got {result}"


def test_determine_date_range_valid_dates() -> None:
    """
    Test that `determine_date_range` correctly returns a range when valid start and end dates are provided.
    """

    start_date = "2023-12-01"
    end_date = "2023-12-15"

    expected_start_date = convert_to_date(start_date)
    expected_end_date = convert_to_date(end_date)

    result_start, result_end = determine_date_range(
        start_date=start_date, end_date=end_date, time_range=None
    )

    assert (
        result_start == expected_start_date
    ), f"Expected {expected_start_date}, got {result_start}"

    assert (
        result_end == expected_end_date
    ), f"Expected {expected_end_date}, got {result_end}"


def test_determine_date_range_invalid_date_order() -> None:
    """
    Test that `determine_date_range` raises a ValueError when start_date is after end_date.
    """

    start_date = "2023-12-15"
    end_date = "2023-12-01"

    with pytest.raises(ValueError, match="Start date cannot be greater than end date"):
        determine_date_range(start_date=start_date, end_date=end_date, time_range=None)


def test_determine_date_range_missing_parameters() -> None:
    """
    Test that `determine_date_range` raises a ValueError when no time range or dates are provided.
    """

    with pytest.raises(
        ValueError,
        match="Either a time range or both start and end dates must be provided",
    ):
        determine_date_range(start_date=None, end_date=None, time_range=None)


def test_determine_date_range_partial_dates() -> None:
    """
    Test that `determine_date_range` raises a ValueError when only one of the start_date or end_date is provided.
    """

    with pytest.raises(
        ValueError,
        match="Either a time range or both start and end dates must be provided",
    ):
        determine_date_range(start_date="2023-12-01", end_date=None, time_range=None)

    with pytest.raises(
        ValueError,
        match="Either a time range or both start and end dates must be provided",
    ):
        determine_date_range(start_date=None, end_date="2023-12-15", time_range=None)
