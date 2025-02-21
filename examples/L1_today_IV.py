from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Region, Tier, TimeRange

licitpy = Licitpy()


tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .in_region(Region.IV)
    .limit(15)
)


for tender in tenders:

    print(f"URL: {tender.url}")

    pprint(
        {
            "url": tender.url,
            "code": tender.code,
            "title": tender.title,
            "status": tender.status,
            "opening_date": tender.opening_date,
            "region": tender.region,
            "subcontracting": tender.subcontracting,
            "is_renewable": tender.is_renewable,
        }
    )
