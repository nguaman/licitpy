from pprint import pprint

from licitpy import Licitpy
from licitpy.types import TimeRange

licitpy = Licitpy()


purchase_orders = licitpy.purchase_orders.from_date(
    time_range=TimeRange.THIS_MONTH
).limit(30)


for purchase_order in purchase_orders:

    pprint(
        {
            "code": purchase_order.code,
            "title": purchase_order.title,
            "commune": purchase_order.commune,
            "region": purchase_order.region,
            "status": purchase_order.status,
            "issue_date": purchase_order.issue_date,
            "url": purchase_order.url,
        }
    )
