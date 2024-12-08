from pprint import pprint

from licitpy import Licitpy
from licitpy.entities.tender import Tender

licitpy = Licitpy()

purchase_order = licitpy.purchase_orders.from_code("750301-261-SE24")

print("Purchase order:")
pprint(
    {
        "url": purchase_order.url,
        "code": purchase_order.code,
        "title": purchase_order.title,
        "status": purchase_order.status,
    }
)

if tender_code := purchase_order.tender_code:

    print(f"Purchase order {purchase_order.code} is related to tender {tender_code}")

    tender = Tender(purchase_order.tender_code)

    pprint(
        {
            "tender": {
                "url": tender.url,
                "code": tender.code,
                "title": tender.title,
                "status": tender.status,
            }
        }
    )

    purchase_orders_related = tender.purchase_orders

    print(f"Purchase orders related to tender {tender.code}:")

    for purchase_order in purchase_orders_related:
        print(
            f"  - {purchase_order.code}: {purchase_order.title} - {purchase_order.status}"
        )
