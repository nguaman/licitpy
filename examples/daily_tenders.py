from licitpy import Licitpy
from licitpy.types.search import TimeRange
from licitpy.types.tender.status import Status

licitpy = Licitpy()

tenders = licitpy.tenders.from_date(time_range=TimeRange.TODAY).with_status(
    Status.PUBLISHED
)

print(f"Total tenders: {tenders.count()}")

for tender in tenders:
    print(f"{tender.code} - {tender.title}")
