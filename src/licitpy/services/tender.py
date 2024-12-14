from datetime import datetime
from functools import partial
from typing import List, Optional
from zoneinfo import ZoneInfo

from pydantic import HttpUrl

from licitpy.downloader.tender import TenderDownloader
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.parsers.tender import TenderParser
from licitpy.types.attachments import Attachment
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Item, Question, Region, TenderFromSource, Tier


class TenderServices:

    def __init__(
        self,
        downloader: Optional[TenderDownloader] = None,
        parser: Optional[TenderParser] = None,
    ):

        self.downloader: TenderDownloader = downloader or TenderDownloader()
        self.parser: TenderParser = parser or TenderParser()

    def verify_status(
        self, status: Status, closing_date: datetime, code: str
    ) -> Status:
        """
        Verify the status of the tender.
        """

        # If the tender is published (active) but the closing date has passed,
        # the status must be verified using the status from the html.

        # This is because 'active' indicates that the bidding process is proceeding normally.
        # However, 'active' can also mean that the bidding has already closed and does not necessarily
        # indicate that it is in the 'published' state.

        is_open = self.is_open(closing_date)

        if status == Status.PUBLISHED and not is_open:

            html = self.get_html_from_code(code)
            status_from_image = self.parser.get_tender_status_from_html(html)

            # StatusFromImage.PUBLISHED -> Status.PUBLISHED
            return Status(status_from_image.name)

        return status

    def get_status(self, data: OpenContract) -> Status:
        """
        Get the status from the Open Contract (OCDS) data.
        """
        code = self.parser.get_tender_code_from_tender_ocds_data(data)
        closing_date = self.get_closing_date(data)

        # We standardize the status provided by the OCDS data with the standardized status.
        # StatusFromOpenContract.PUBLISHED -> Status.PUBLISHED
        status = Status(self.parser.get_tender_status_from_tender_ocds_data(data).name)

        # If the tender is published (active) but the closing date has passed,
        # the status must be verified using the status from the html.
        return self.verify_status(status, closing_date, code)

    def get_ocds_data(self, code: str) -> OpenContract:
        """
        Get the Open Contract Data (OCDS) from the tender code.
        """

        return self.downloader.get_tender_ocds_data_from_api(code)

    def get_url(self, code: str) -> HttpUrl:
        """
        Get the URL from the tender code.
        """

        return self.downloader.get_tender_url_from_code(code)

    def get_title(self, data: OpenContract) -> str:
        """
        Get the title from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_title_from_tender_ocds_data(data)

    def get_opening_date(self, data: OpenContract) -> datetime:
        """
        Get the opening date from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_opening_date_from_tender_ocds_data(data)

    def get_html(self, url: HttpUrl) -> str:
        """
        Get the HTML from the URL.
        """

        return self.downloader.get_html_from_url(url)

    def get_tenders_from_sources(self, year: int, month: int) -> List[TenderFromSource]:

        # # We retrieve the tenders from both the API (OCDS) and the CSV (Massive Download).
        tenders_consolidated = self.downloader.get_consolidated_tender_data(year, month)

        # Get the OCDS data for each tender
        data_tenders = self.downloader.get_tender_ocds_data_from_codes(
            tenders_consolidated
        )

        tenders_from_source: List[TenderFromSource] = []

        # Enrich the tender data with information from OCDS
        for tender_consolidated in tenders_consolidated:

            # Filtering tenders that are internal QA tests from Mercado Publico.
            # eg: 500977-191-LS24 : Nombre Unidad : MpOperaciones
            if tender_consolidated.code.startswith("500977-"):
                continue

            # Retrieve the OCDS data for the current tender
            data = data_tenders[tender_consolidated.code]

            # Get the opening date in datetime format
            opening_date = self.parser.get_tender_opening_date_from_tender_ocds_data(
                data
            )

            # Retrieve the tender status, which needs to be verified at a later stage.
            # This is because the status from OCDS may have different meanings compared to those displayed on the website.
            status = tender_consolidated.status or Status(
                self.parser.get_tender_status_from_tender_ocds_data(data).name
            )

            # Retrieve the tender region
            region = self.parser.get_tender_region_from_tender_ocds_data(data)

            # Get the closing date in datetime format
            closing_date = self.get_closing_date(data)

            tenders_from_source.append(
                TenderFromSource(
                    code=tender_consolidated.code,
                    status=status,
                    region=region,
                    opening_date=opening_date,
                    closing_date=closing_date,
                )
            )

        return sorted(
            tenders_from_source, key=lambda tender: tender.opening_date, reverse=True
        )

    def get_tier(self, code: str) -> Tier:
        """
        Get the budget tier from the tender code.
        """

        return self.parser.get_tender_tier(code)

    def get_description(self, data: OpenContract) -> str:
        """
        Get the description from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_description_from_tender_ocds_data(data)

    def get_region(self, data: OpenContract) -> Region:
        """
        Get the region from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_region_from_tender_ocds_data(data)

    def get_closing_date(self, data: OpenContract) -> datetime:
        """
        Get the closing date from the Open Contract (OCDS) data.
        """

        closing_date = self.parser.get_closing_date_from_tender_ocds_data(data)

        if closing_date is not None:
            return closing_date

        # If the closing date is not available in the OCDS data, we retrieve it from the HTML.
        code = self.parser.get_tender_code_from_tender_ocds_data(data)
        html = self.get_html_from_code(code)

        # Get the closing date from the HTML
        return self.parser.get_closing_date_from_html(html)

    def get_code_from_ocds_data(self, data: OpenContract) -> str:
        """
        Get the tender code from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_code_from_tender_ocds_data(data)

    def is_open(self, closing_date: datetime) -> bool:
        """
        Check if the tender is still open.
        """

        if not closing_date:
            return False

        now_utc = datetime.now(tz=ZoneInfo("America/Santiago"))

        return now_utc < closing_date

    def get_html_from_code(self, code: str) -> str:
        """
        Get the HTML from the tender code.
        """

        url = self.get_url(code)

        return self.get_html(url)

    def get_html_from_ocds_data(self, data: OpenContract) -> str:
        """
        Get the HTML from the tender code in the Open Contract data.
        """

        code = self.parser.get_tender_code_from_tender_ocds_data(data)

        return self.get_html_from_code(code)

    def get_attachment_url(self, html: str) -> HttpUrl:
        """
        Get the attachment URL from the HTML.
        """

        return self.parser.get_attachment_url_from_html(html)

    def get_attachments_from_url(self, url: HttpUrl) -> List[Attachment]:
        """
        Get the attachments from the URL.
        """

        html = self.downloader.get_html_from_url(url)
        attachments: List[Attachment] = self.parser.get_attachments(html)

        for attachment in attachments:

            download_attachment_fn = partial(
                self.downloader.download_attachment, url, attachment
            )

            attachment._download_fn = download_attachment_fn

        return attachments

    def get_signed_base_from_attachments(
        self, attachments: List[Attachment]
    ) -> Attachment:
        """
        Get the signed base from the attachments.
        """

        signed_bases = [
            attachment
            for attachment in attachments
            if "Anexo Resolucion Electronica (Firmada)" in attachment.type
        ]

        if not signed_bases:
            raise ValueError("No signed base found in attachments.")

        return signed_bases[0]

    def get_tender_purchase_order_url(self, html: str) -> HttpUrl:
        """
        Get the purchase order URL from the HTML.
        """

        return self.parser.get_tender_purchase_order_url(html)

    def get_tender_purchase_orders(self, html: str) -> PurchaseOrders:
        """
        Get the purchase orders from the HTML.
        """

        url = self.get_tender_purchase_order_url(html)

        html = self.downloader.get_html_from_url(url)
        codes = self.parser.get_purchase_orders_codes_from_html(html)

        # Create the purchase orders from the codes obtained from the HTML of the tender.
        return PurchaseOrders.from_tender(codes)

    def get_questions_url(self, html: str) -> HttpUrl:
        """
        Get the questions URL from the HTML.
        """

        return self.parser.get_questions_url(html)

    def get_questions(self, url: HttpUrl) -> List[Question]:
        """
        Get the questions from the URL.
        """

        html = self.downloader.get_html_from_url(url)
        code = self.parser.get_question_code(html)

        return self.downloader.get_tender_questions(code)

    def get_items(self, html: str) -> List[Item]:
        """
        Get the items from the HTML.
        """

        codes = self.parser.get_item_codes_from_html(html)

        return [self.parser.get_item_from_code(html, code) for code in codes]
