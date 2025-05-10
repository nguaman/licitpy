import asyncio

from licitpy import Licitpy
from licitpy.core.entities.tender import Tender
from licitpy.core.enums import Country


async def main() -> None:
    async with Licitpy(use_cache=False) as licitpy:

        tender = licitpy[Country.CL].get("2392-20-LR25")
        
        print(f"Tender Url: {tender.url()}")
        print(f"Content Length: {len(tender.html())}")

        tender_codes = {
            Country.CL: [
                "2392-20-LR25",
                "2770-39-LR25",
                "3668-12-H225",
                "2767-29-LR25",
                "4099-12-LQ25",
                "3668-14-H225",
                "5251-71-LE25",
                "438-40-LQ25",
                "2490-30-LP25",
                "2392-22-LE25",
            ],
            Country.EU: [
                "275748-2025",
                "275311-2025",
                "273285-2025",
                "272419-2025",
                "269468-2025",
                "269085-2025",
                "268233-2025",
                "264942-2025",
                "262215-2025",
                "259989-2025",
            ],
        }

        tenders: list[Tender] = []
        for country, codes in tender_codes.items():
            tenders.extend([licitpy[country].get(code) for code in codes])

        urls = await asyncio.gather(*[tender.ahtml() for tender in tenders])

        for tender, html in zip(tenders, urls):
            print(
                f"Country: {tender.country}, Tender Code: {tender.code}, Content Length: {len(html)} {tender.url()}"
            )


if __name__ == "__main__":
    asyncio.run(main())
