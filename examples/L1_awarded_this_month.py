from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Status, Tier
from licitpy.types.search import TimeRange

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .with_status(Status.AWARDED)
    .limit(10)
)


for tender in tenders:
    pprint(
        {
            "code": tender.code,
            "title": tender.title,
            "status": tender.status,
            "opening_date": tender.opening_date,
        }
    )
