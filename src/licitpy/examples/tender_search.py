import asyncio
from typing import AsyncIterator, Iterator

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from licitpy import Licitpy
from licitpy.core.entities.tender import Tender


async def main() -> None:

    console = Console()
    table = Table(show_header=True)
    table.add_column("Tender Code")
    table.add_column("Country")
    table.add_column("Publication Date")

    layout = Layout()
    layout.split(
        Layout(
            Panel(
                Spinner(
                    "dots", text=Text(" Loading tender data...", style="bold green")
                )
            ),
            name="status",
            size=3,
        ),
        Layout(Panel(table, title="Tender Results")),
    )

    async with Licitpy(use_cache=True) as licitpy:

        with Live(layout, console=console, refresh_per_second=1):

            # tenders: Iterator[Tender] = (
            #     licitpy.cl.search().published_on("2025-05-02").limit(3).all()
            # )

            tenders: AsyncIterator[Tender] = (
                licitpy.cl.search().published_on("2025-05-08").limit(10).aall()
            )

            # for tender in tenders:
            count = 0
            async for tender in tenders:
                pub_date = await tender.apublication_date()
                table.add_row(tender.code, str(tender.country), str(pub_date.date()))

                count += 1

            layout["status"].update(
                Panel(
                    Text(f"✓ Loaded {count} tenders successfully!", style="bold green")
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
