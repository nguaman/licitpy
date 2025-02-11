from pprint import pprint

from licitpy import Licitpy
from licitpy.types.tender.status import Status

licitpy = Licitpy()

tender = licitpy.tenders.from_code("3000-104-LE24")

pprint(
    {
        "url": tender.url,
        "code": tender.code,
        "title": tender.title,
        "status": tender.status,
        "opening_date": tender.opening_date,
        "closing_date": tender.closing_date,
        "region": tender.region,
    }
)

print(" Items ".center(80, "="))
pprint(tender.items)


if tender.status is Status.AWARDED:
    print(" Awarded ".center(80, "="))

    award = tender.award

    pprint(
        {
            "method": award.method,
            "url": award.url,
            "award_amount": award.award_amount,
            "estimated_amount": award.estimated_amount,
        }
    )
