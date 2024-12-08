from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Status, Tier
from licitpy.types.geography import Region
from licitpy.types.search import TimeRange

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .with_status(Status.AWARDED)
    .in_region(Region.IV)
    .limit(10)
)


for tender in tenders:
    pprint(
        {
            "code": tender.code,
            "region": tender.region,
            "status": tender.status,
            "purchase_orders": [
                {
                    "code": purchase_order.code,
                    "status": purchase_order.status,
                    "title": purchase_order.title,
                    "url": purchase_order.url,
                }
                for purchase_order in tender.purchase_orders
            ],
        }
    )
