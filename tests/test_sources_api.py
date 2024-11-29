from datetime import date

import pytest

from licitpy.sources.api import API


@pytest.fixture
def api_instance() -> API:
    return API(api_key="licitpy-")


def test_api_initialization(api_instance: API) -> None:
    assert api_instance.api_key == "licitpy-"


def test_get_monthly_tenders_not_implemented(api_instance: API) -> None:
    with pytest.raises(
        NotImplementedError, match="This method has not been implemented yet."
    ):
        api_instance.get_monthly_tenders(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 31)
        )


def test_get_tender_not_implemented(api_instance: API) -> None:
    with pytest.raises(
        NotImplementedError, match="This method has not been implemented yet."
    ):
        api_instance.get_tender(code="3955-54-LE24")
