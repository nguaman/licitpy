from datetime import date

import pytest

from licitpy.sources.api import API


@pytest.fixture
def api_instance():
    """Fixture to provide an API instance with a predefined API key."""
    return API(api_key="licitpy-")


def test_api_initialization(api_instance):
    """Test that the API instance is initialized with the correct API key."""
    assert api_instance.api_key == "licitpy-", "API key should be set correctly"


@pytest.mark.parametrize(
    "start_date, end_date, limit",
    [
        (date(2024, 1, 1), date(2024, 1, 31), None),  # No limit provided
        (date(2024, 1, 1), date(2024, 1, 31), 10),  # Limit provided
    ],
)
def test_get_monthly_tenders_not_implemented(api_instance, start_date, end_date, limit):
    """
    Test that get_monthly_tenders raises NotImplementedError.
    This ensures the method is not yet implemented.
    """
    with pytest.raises(
        NotImplementedError, match="This method has not been implemented yet."
    ):
        if limit is None:
            api_instance.get_monthly_tenders(start_date, end_date)
        else:
            api_instance.get_monthly_tenders(start_date, end_date, limit)
