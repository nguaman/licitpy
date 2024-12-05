from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Region, Status, Tier
from licitpy.types.search import TimeRange

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.THIS_MONTH)
    .by_budget_tier(Tier.L1)
    .with_status(Status.PUBLISHED)
    .in_region(Region.IV)
    .limit(3)
)


for tender in tenders:

    pprint(
        {
            "code": tender.code,
            "region": tender.region,
            "status": tender.status,
            "attachment_url": tender.attachment_url,
        }
    )

    attachments = tender.attachments
    total_attachments = len(attachments)

    for index, attachment in enumerate(attachments, 1):

        name = attachment.name

        print(f"Attachment {index}/{total_attachments} - {name}\n")

        # The file type is inferred from the file extension
        file_type = attachment.file_type

        pprint(
            {
                "name": attachment.name,
                "description": attachment.description,
                "size": attachment.size,
                "upload_date": attachment.upload_date,
                "file_type": file_type,
                "content_status": attachment.content_status,
            }
        )

        print(f"Downloading {name}...\n")
        content_base64 = attachment.content

        # Do something with the content
        # ...

        print(f"Current Status: {attachment.content_status}\n")
