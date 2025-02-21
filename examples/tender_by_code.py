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

attachments = tender.attachments

if attachments:
    print(" Attachments ".center(80, "="))
    for attachment in attachments:
        pprint(
            {
                "name": attachment.name,
                "description": attachment.description,
                "type": attachment.type,
                "size": attachment.size,
                "upload_date": attachment.upload_date,
                "file_type": attachment.file_type,
            }
        )

        # Download attachment
        # content = attachment.content
        # with open(attachment.name, "wb") as f:
        #     f.write(attachment.content)


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

    award_attachments = award.attachments

    if award_attachments:

        print(" Award Attachments ".center(80, "="))

        for award_attachment in award_attachments:
            pprint(
                {
                    "name": award_attachment.name,
                    "description": award_attachment.description,
                    "type": award_attachment.type,
                    "size": award_attachment.size,
                    "upload_date": award_attachment.upload_date,
                    "file_type": award_attachment.file_type,
                }
            )

results = award.results

if results:
    print(" Results ".center(80, "="))

    for item in results.items:

        print(" Item ".center(80, "="))

        pprint(
            {
                "item_index": item.item_index,
                "item_name": item.item_name,
                "item_description": item.item_description,
                "item_onu": item.item_onu,
                "item_quantity": item.item_quantity,
                "item_total_awarded_amount": item.item_total_awarded_amount,
            }
        )

        print(" Suppliers ".center(80, "="))

        for supplier in item.suppliers:
            pprint(
                {
                    "supplier_name": supplier.supplier_name,
                    "supplier_item_description": supplier.supplier_item_description,
                    "supplier_bid_total_price": supplier.supplier_bid_total_price,
                    "supplier_awarded_quantity": supplier.supplier_awarded_quantity,
                    "supplier_total_awarded_amount": supplier.supplier_total_awarded_amount,
                    "supplier_bid_result": supplier.supplier_bid_result,
                }
            )
