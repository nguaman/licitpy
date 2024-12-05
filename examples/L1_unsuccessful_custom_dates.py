from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Status, Tier

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(start_date="2024-11-12", end_date="2024-11-21")
    .by_budget_tier(Tier.L1)
    .with_status(Status.UNSUCCESSFUL)
    .limit(50)
)


for tender in tenders:
    pprint(
        {
            "code": tender.code,
            "title": tender.title,
            "description": tender.description,
            "status": tender.status,
            "opening_date": tender.opening_date,
        }
    )
