from typing import List

import lxml.html
from lxml.html import HtmlElement


class ElementNotFoundException(Exception):
    pass


class BaseParser:

    def get_html_element(self, html: str) -> HtmlElement:
        return lxml.html.fromstring(html)

    def get_html_element_by_id(self, html: str, element_id: str) -> List[HtmlElement]:
        html: HtmlElement = self.get_html_element(html)
        element: HtmlElement = html.xpath(f'//*[@id="{element_id}"]')

        return element

    def get_attribute_by_element_id(
        self, html: str, element_id: str, attribute: str
    ) -> str:

        html_element: List[HtmlElement] = self.get_html_element_by_id(html, element_id)

        if not html_element:
            raise ElementNotFoundException(f"Element with ID '{element_id}' not found")

        attribute_elements = html_element[0].xpath(f".//{attribute}")
        value: str = attribute_elements[0]

        return value.strip()

    def get_text_by_element_id(self, html: str, element_id: str) -> str:
        return self.get_attribute_by_element_id(html, element_id, "text()")

    def get_view_state(self, html: str) -> str:
        return self.get_attribute_by_element_id(html, "__VIEWSTATE", "@value")
