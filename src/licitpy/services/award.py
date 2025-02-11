from typing import Optional
from pydantic import HttpUrl

from licitpy.downloader.award import AwardDownloader
from licitpy.parsers.award import AwardParser
from licitpy.types.award import Method


class AwardServices:

    def __init__(
        self,
        downloader: Optional[AwardDownloader] = None,
        parser: Optional[AwardParser] = None,
    ):

        self.downloader = downloader or AwardDownloader()
        self.parser = parser or AwardParser()

    def get_html(self, url: HttpUrl) -> str:
        """
        Get the HTML content of a award given its URL.
        """

        return self.downloader.get_html_from_url(url)

    def get_url(self, html: str) -> HttpUrl:
        """
        Get the URL of a purchase order given its code.
        """
        return self.parser.get_url_from_html(html)

    def get_method(self, html: str) -> Method:
        """
        Get the method of a purchase order given its code.
        """
        return self.parser.get_method_from_html(html)

    def get_award_amount(self, html: str) -> float:
        """
        Field : Monto Neto Adjudicado

        Get the amount of an award given its HTML content.
        """

        return self.parser.get_award_amount_from_html(html)

    def get_estimated_amount(self, html: str) -> float:
        """
        Field: Monto Neto Estimado del Contrato

        Get the estimated amount of an award given its HTML content.
        """
        return self.parser.get_estimated_amount_from_html(html)
