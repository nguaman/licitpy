import asyncio
from pprint import pprint

from licitpy.licitpy import Licitpy


async def main() -> None:
    async with Licitpy() as client:
        # Download the monthly bulk file for October 2023
        file = await client.eu.download_monthly_bulk_file(when="2023-10")
        pprint(file)

        # Download the entire year 2015
        files = await client.eu.download_yearly_bulk_file(
            year="2015"
        )
        
        pprint(files)


if __name__ == "__main__":
    asyncio.run(main())
