from datetime import date
from typing import List

import pytest

from licitpy.client.licitpy import Licitpy
from licitpy.entities.tender import Tender
from licitpy.sources.api import API
from licitpy.sources.local import Local
from licitpy.types.geography import Region
from licitpy.types.tender.status import Status


@pytest.fixture
def sample_tenders() -> List[Tender]:
    """ Returns a list of sample tenders """
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


def test_licitpy_initialization_with_api_key() -> None:
    """ Test the initialization of the Licitpy client with an API key """
    api_key = "licitpy-"
    licitpy = Licitpy(api_key=api_key)

    assert isinstance(licitpy.source, API)
    assert licitpy.source.api_key == api_key


def test_licitpy_initialization_without_api_key() -> None:
    """ Test the initialization of the Licitpy client without an API key """
    licitpy = Licitpy()

    assert isinstance(licitpy.source, Local)


def test_licitpy_tenders_client() -> None:
    """ Test the initialization of the tenders client """
    api_key = "licitpy-"
    licitpy = Licitpy(api_key=api_key)

    tenders_client = licitpy.tenders

    assert tenders_client is not None
    assert tenders_client.source == licitpy.source


def test_licitpy_purchase_orders_client() -> None:
    """ Test the initialization of the purchase orders client """
    api_key = "licitpy-"
    licitpy = Licitpy(api_key=api_key)

    purchase_orders_client = licitpy.purchase_orders

    assert purchase_orders_client is not None
    assert purchase_orders_client.source == licitpy.source
