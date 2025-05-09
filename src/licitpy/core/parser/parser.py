import lxml.html
from lxml.etree import ParserError, XMLSyntaxError
from lxml.html import HtmlElement


class BaseParser:

    def get_html_element(self, html: str) -> HtmlElement:
        try:

            element = lxml.html.fromstring(html)
            return element

        except (ParserError, XMLSyntaxError) as e:
            raise ValueError("Document is empty or invalid") from e
