import asyncio

from licitpy import Licitpy
from licitpy.core.entities.tender import Tender


async def main() -> None:
    async with Licitpy(use_cache=False) as licitpy:

        # Fetch a single tender asynchronously
        tender = licitpy.cl.get("2392-20-LR25")
        print(tender.url())

        # 
        tender_codes = [
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
        ]

        tenders: list[Tender] = [licitpy.cl.get(code) for code in tender_codes]
        urls = await asyncio.gather(*[tender.aurl() for tender in tenders])

        for tender, url in zip(tenders, urls):
            print(f"Tender Code: {tender.code}, URL: {url}")


if __name__ == "__main__":
    asyncio.run(main())
