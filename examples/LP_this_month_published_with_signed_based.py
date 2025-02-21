from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Status, Tier, TimeRange

licitpy = Licitpy()


tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.LE)
    .with_status(Status.PUBLISHED)
)


print(f"Found {tenders.count()} tenders.")

for tender in tenders:

    print(f"Checking tender {tender.code}...")

    if not tender.has_signed_base:
        continue

    pprint(
        {
            "url": tender.url,
            "code": tender.code,
            "title": tender.title,
            "status": tender.status,
            "opening_date": tender.opening_date,
            "region": tender.region,
        }
    )
