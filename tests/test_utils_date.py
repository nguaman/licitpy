from datetime import date

import pytest

from licitpy.utils.date import convert_to_date


class TestConvertToDate:
    @pytest.mark.parametrize(
        "date_value, expected_date",
        [
            ("2024-01-01", date(2024, 1, 1)),
            ("2023-12-31", date(2023, 12, 31)),
            (date(2024, 1, 1), date(2024, 1, 1)),
            (date(2023, 12, 31), date(2023, 12, 31)),
        ],
    )
    def test_convert_to_date(self, date_value: str | date, expected_date: date) -> None:
        """
        Test that `convert_to_date` correctly converts string and date inputs to date objects.
        """
        result = convert_to_date(date_value)
        assert result == expected_date, f"Expected {expected_date}, got {result}"

    def test_convert_to_date_invalid_string(self) -> None:
        """
        Test that `convert_to_date` raises a ValueError for invalid date strings.
        """
        with pytest.raises(ValueError):
            convert_to_date("invalid-date")

    def test_convert_to_date_none(self) -> None:
        """
        Test that `convert_to_date` raises a TypeError when None is passed.
        """
        with pytest.raises(TypeError):
            convert_to_date(None)  # type: ignore[arg-type]

    def test_convert_to_date_empty_string(self) -> None:
        """
        Test that `convert_to_date` raises a ValueError for empty date strings.
        """
        with pytest.raises(ValueError):
            convert_to_date("")

    def test_convert_to_date_unexpected_type(self) -> None:
        """
        Test that `convert_to_date` raises a TypeError for unexpected input types.
        """
        with pytest.raises(TypeError):
            convert_to_date(12345)  # type: ignore[arg-type]
