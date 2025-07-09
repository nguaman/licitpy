import asyncio

from licitpy.licitpy import Licitpy


async def main() -> None:
    async with Licitpy() as client:

        tender_codes = [
            "1057501-353-LE25",
            "1057501-337-LE25",
            "1057501-342-LE25",
            "1057501-343-LE25",
            "1057501-323-LE25",
            "1057501-334-LE25",
            "1057501-363-LE25",
            "1057501-372-LE25",
            "1057501-374-LE25",
            "948806-66-LP25",
        ]

        tenders = await asyncio.gather(
            *[client.cl.get_by_code(code) for code in tender_codes]
        )

        for tender in tenders:
            print(f"Code: {tender.code}")
            print(f"Title: {tender.title}")


if __name__ == "__main__":
    asyncio.run(main())
