from datetime import date
from typing import List

import pytest

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Region, Tier


@pytest.fixture
def sample_tenders() -> List[Tender]:
    """Return a list of sample tenders"""
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
def tenders(sample_tenders: List[Tender]) -> Tenders:
    """Return a Tenders instance with sample tenders"""
    return Tenders(sample_tenders)


def test_by_budget_tier(tenders: Tenders) -> None:
    """Test by_budget_tier method"""
    result = tenders.by_budget_tier(Tier.L1)

    assert isinstance(result, Tenders), "Expected result to be an instance of Tenders"
    assert result.count() == 1, "Expected one tender with Tier.L1"


def test_with_status(tenders: Tenders) -> None:
    """Test with_status method"""
    result = tenders.with_status(Status.PUBLISHED)

    assert isinstance(result, Tenders), "Expected result to be an instance of Tenders"
    assert result.count() == 3, "Expected 3 tenders with status PUBLISHED"


def test_in_region(tenders: Tenders) -> None:
    """Test in_region method"""
    result = tenders.in_region(Region.RM)

    assert isinstance(result, Tenders), "Expected result to be an instance of Tenders"
    assert result.count() == 2, "Expected 2 tenders in region RM"


def test_to_pandas_not_implemented(tenders: Tenders) -> None:
    """Test to_pandas method"""

    with pytest.raises(NotImplementedError):
        tenders.to_pandas()


def test_from_tenders(sample_tenders: List[Tender]) -> None:
    """Test from_tenders method"""
    result = Tenders.from_tenders(sample_tenders)

    assert isinstance(result, Tenders), "Expected result to be an instance of Tenders"
    assert result.count() == 4, "Expected 4 tenders"


def test_codes(tenders: Tenders) -> None:
    """Test codes property"""
    result = tenders.codes
    expected_codes = ["750301-54-L124", "4326-1-LR24", "3955-54-LE24", "2513-2-LE24"]

    assert result == expected_codes, f"Expected {expected_codes}, got {result}"


def test_limit(tenders: Tenders) -> None:
    """Test limit method"""
    result = tenders.limit(2)

    assert isinstance(result, Tenders), "Expected result to be an instance of Tenders"
    assert result.count() == 2, "Expected 2 tenders"


def test_count(tenders: Tenders) -> None:
    """Test count method"""
    result = tenders.count()

    assert result == 4, "Expected count to be 4"


def test_iter(tenders: Tenders) -> None:
    """Test __iter__ method"""
    result = list(iter(tenders))

    assert len(result) == 4, "Expected 4 tenders"
    assert all(
        isinstance(tender, Tender) for tender in result
    ), "Expected all items to be instances of Tender"
