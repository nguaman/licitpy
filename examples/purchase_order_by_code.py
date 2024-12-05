from pprint import pprint

from licitpy import Licitpy

licitpy = Licitpy()

tender = licitpy.purchase_orders.from_code("1271359-358-SE24")

pprint(
    {
        "url": tender.url,
        "code": tender.code,
        "title": tender.title,
        "status": tender.status,
    }
)
