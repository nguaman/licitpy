from pprint import pprint

from licitpy import Licitpy

licitpy = Licitpy()

tender = licitpy.tenders.from_code("2446-900-L124")

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
