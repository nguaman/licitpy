from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Tier, TimeRange
from licitpy.types.tender import Status

licitpy = Licitpy()

tenders = (
    licitpy.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .with_status(Status.AWARDED)
    .limit(10)
)


data = []
for tender in tenders:
    data.append(
        {
            "code": tender.code,
            "title": tender.title,
            "status": tender.status,
            "opening_date": tender.opening_date,
        }
    )


pprint(data)
