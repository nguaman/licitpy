from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Region, Status, Tier
from licitpy.types.search import TimeRange

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .with_status(Status.PUBLISHED)
    .in_region(Region.IV)
    .limit(10)
)


for tender in tenders:
    pprint(
        {
            "url": tender.url,
            "code": tender.code,
            "region": tender.region,
            "status": tender.status,
        }
    )
