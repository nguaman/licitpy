import pytest
from lxml.html import HtmlElement

from licitpy.parsers.base import BaseParser, ElementNotFoundException


@pytest.fixture
def base_parser():
    """Fixture to provide a BaseParser instance."""
    return BaseParser()


def test_get_html_element(base_parser):
    """Test that get_html_element correctly parses the HTML string into an HtmlElement."""
    html = "<html><body><div id='test'>Content</div></body></html>"
    element = base_parser.get_html_element(html)

    assert isinstance(
        element, HtmlElement
    ), "The returned element should be an instance of HtmlElement"
    assert (
        element.xpath('//*[@id="test"]')[0].text == "Content"
    ), "The content of the element should be 'Content'"


@pytest.mark.parametrize(
    "html, element_id, expected_text",
    [
        ("<html><body><div id='test'>Content</div></body></html>", "test", "Content"),
        (
            "<html><body><div id='sample'>Sample Text</div></body></html>",
            "sample",
            "Sample Text",
        ),
    ],
)
def test_get_html_element_by_id(base_parser, html, element_id, expected_text):
    """Test that get_html_element_by_id retrieves elements with the correct ID."""
    elements = base_parser.get_html_element_by_id(html, element_id)
    assert len(elements) == 1, "There should be one element with the given ID"
    assert elements[0].text == expected_text, f"The content should be '{expected_text}'"


def test_get_html_element_by_id_not_found(base_parser):
    """Test that get_html_element_by_id returns an empty list when the element is not found."""
    html = "<html><body><div id='test'>Content</div></body></html>"
    elements = base_parser.get_html_element_by_id(html, "nonexistent")
    assert len(elements) == 0, "There should be no elements with the given ID"


def test_get_attribute_by_element_id(base_parser):
    """Test that get_attribute_by_element_id retrieves the correct attribute."""
    html = "<html><body><div id='test' class='my-class'>Content</div></body></html>"
    attribute = base_parser.get_attribute_by_element_id(html, "test", "@class")
    assert attribute == "my-class", "The attribute value should be 'my-class'"


def test_get_attribute_by_element_id_not_found(base_parser):
    """Test that get_attribute_by_element_id raises an exception when the element is not found."""
    html = "<html><body><div id='test'>Content</div></body></html>"
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'nonexistent' not found"
    ):
        base_parser.get_attribute_by_element_id(html, "nonexistent", "@class")


def test_get_text_by_element_id(base_parser):
    """Test that get_text_by_element_id retrieves the correct text content."""
    html = "<html><body><div id='test'>Content</div></body></html>"
    text = base_parser.get_text_by_element_id(html, "test")
    assert text == "Content", "The text content should be 'Content'"


def test_get_view_state(base_parser):
    """Test that get_view_state retrieves the correct view state value."""
    html = "<html><body><input type='hidden' id='__VIEWSTATE' value='state-value'/></body></html>"
    view_state = base_parser.get_view_state(html)
    assert view_state == "state-value", "The view state value should be 'state-value'"


def test_get_view_state_not_found(base_parser):
    """Test that get_view_state raises an exception when the view state is not found."""
    html = "<html><body></body></html>"
    with pytest.raises(
        ElementNotFoundException, match="Element with ID '__VIEWSTATE' not found"
    ):
        base_parser.get_view_state(html)
