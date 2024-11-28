from pprint import pprint

from licitpy import Licitpy

licitpy = Licitpy()

tender = licitpy.from_code("3494-210-L124")

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
