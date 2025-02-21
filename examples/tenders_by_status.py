from licitpy import Licitpy
from licitpy.types.tender.status import Status

licitpy = Licitpy()


tenders = licitpy.tenders.from_status(Status.CLOSED)

print(f"Total tenders: {tenders.count()}")
