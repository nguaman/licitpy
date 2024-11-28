from datetime import date

import pytest

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.sources.base import BaseSource


class MockBaseSource(BaseSource):
    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:
        return Tenders([])

    def get_tender(self, code: str) -> Tender:
        return Tender(
            code=code,
            region=None,
            status=None,
            title="",
            description="",
            opening_date=None,
        )


@pytest.fixture
def mock_base_source() -> MockBaseSource:
    return MockBaseSource()


def test_get_monthly_tenders(mock_base_source: MockBaseSource) -> None:
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    tenders = mock_base_source.get_monthly_tenders(
        start_date=start_date, end_date=end_date
    )

    assert isinstance(tenders, Tenders)
    assert len(tenders._tenders) == 0


def test_get_tender(mock_base_source: MockBaseSource) -> None:
    code = "3955-54-LE24"
    tender = mock_base_source.get_tender(code=code)

    assert isinstance(tender, Tender)
    assert tender.code == code
