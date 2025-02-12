import re
from pydantic import HttpUrl
from licitpy.parsers.base import BaseParser
from licitpy.types.award import Method
from licitpy.utils.amounts import amount_to_int


class AwardParser(BaseParser):

    def get_url_from_html(self, html: str) -> HttpUrl:
        """
        Get the URL of an award given its HTML content.
        """

        href = self.get_href_by_element_id(html, "imgAdjudicacion")
        match = re.search(r"qs=(.*)$", href)

        if not match:
            raise ValueError("Awarded query string not found")

        qs = match.group(1)
        url = f"https://www.mercadopublico.cl/Procurement/Modules/RFB/StepsProcessAward/PreviewAwardAct.aspx?qs={qs}"

        return HttpUrl(url)

    def get_method_from_html(self, html: str) -> Method:
        """
        Get the method of an award given its HTML content.
        """

        return Method(self.get_text_by_element_id(html, "lblAwardTypeShow"))

    def get_award_amount_from_html(self, html: str) -> int:
        """
        Get the amount of an award given its HTML content.
        """

        amount = self.get_text_by_element_id(html, "lblAmountShow")
        return amount_to_int(amount)

    def get_estimated_amount_from_html(self, html: str) -> int:
        """
        Get the estimated amount of an award given its HTML content.
        """

        amount = self.get_text_by_element_id(html, "lblEstimatedAmountShow")
        return amount_to_int(amount)


