from datetime import date

import pytest

from licitpy.utils.date import convert_to_date


def test_convert_valid_string_to_date():
    """
    Test that a valid date string is correctly converted to a `date` object.
    """
    date_str = "2023-10-01"
    expected_date = date(2023, 10, 1)
    result = convert_to_date(date_str)
    assert result == expected_date, f"Expected {expected_date}, got {result}"


def test_convert_to_date_with_invalid_format():
    """
    Test that an invalid date format raises a `ValueError`.
    """
    invalid_date_str = "11/16/2024"  # Incorrect format
    with pytest.raises(ValueError, match="Invalid isoformat string: '.*'"):
        convert_to_date(invalid_date_str)
