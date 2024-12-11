from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Tier
from licitpy.types.search import TimeRange

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .limit(100)
)


for index, tender in enumerate(tenders, 1):

    print(f" {index} - Tender ".center(120, "="))

    pprint(
        {
            "url": tender.url,
            "code": tender.code,
            "region": tender.region,
            "status": tender.status,
            "opening_date": tender.opening_date,
            "closing_date": tender.closing_date,
        }
    )

    print(" Items ".center(80, "="))
    pprint(tender.items)
