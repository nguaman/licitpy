import pytest
from lxml.html import HtmlElement

from licitpy.parsers.base import BaseParser, ElementNotFoundException


@pytest.fixture
def base_parser() -> BaseParser:
    """Fixture to provide a BaseParser instance."""
    return BaseParser()


@pytest.fixture
def example_html() -> str:
    """Fixture to provide example HTML content."""
    return """
    <html>
        <body>
            <div id='test'>Content</div>
            <div id='sample'>Sample Text</div>
            <div id='test2' class='my-class'>Another Content</div>
            <input type='hidden' id='__VIEWSTATE' value='state-value'/>
            <img id="imgEstado" src="../../Includes/images/FichaLight/iconos_estados/desierta.png" style="border-width:0px;">
        </body>
    </html>
    """


def test_get_html_element(base_parser: BaseParser, example_html: str) -> None:
    """Test that get_html_element correctly parses the HTML string into an HtmlElement."""
    element = base_parser.get_html_element(example_html)
    assert isinstance(
        element, HtmlElement
    ), "The returned element should be an instance of HtmlElement"
    assert (
        element.xpath('//*[@id="test"]')[0].text == "Content"
    ), "The content of the element should be 'Content'"


@pytest.mark.parametrize(
    "element_id, expected_text",
    [
        ("test", "Content"),
        ("sample", "Sample Text"),
    ],
)
def test_get_html_element_by_id(
    base_parser: BaseParser, example_html: str, element_id: str, expected_text: str
) -> None:
    """Test that get_html_element_by_id retrieves elements with the correct ID."""
    elements = base_parser.get_html_element_by_id(example_html, element_id)
    assert len(elements) == 1, "There should be one element with the given ID"
    assert elements[0].text == expected_text, f"The content should be '{expected_text}'"


def test_get_html_element_by_id_not_found(
    base_parser: BaseParser, example_html: str
) -> None:
    """Test that get_html_element_by_id returns an empty list when the element is not found."""
    elements = base_parser.get_html_element_by_id(example_html, "nonexistent")
    assert len(elements) == 0, "There should be no elements with the given ID"


def test_get_attribute_by_element_id(
    base_parser: BaseParser, example_html: str
) -> None:
    """Test that get_attribute_by_element_id retrieves the correct attribute."""
    attribute = base_parser.get_attribute_by_element_id(example_html, "test2", "@class")
    assert attribute == "my-class", "The attribute value should be 'my-class'"


def test_get_attribute_by_element_id_not_found(
    base_parser: BaseParser, example_html: str
) -> None:
    """Test that get_attribute_by_element_id raises an exception when the element is not found."""
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'nonexistent' not found"
    ):
        base_parser.get_attribute_by_element_id(example_html, "nonexistent", "@class")


def test_get_text_by_element_id(base_parser: BaseParser, example_html: str) -> None:
    """Test that get_text_by_element_id retrieves the correct text content."""
    text = base_parser.get_text_by_element_id(example_html, "test")
    assert text == "Content", "The text content should be 'Content'"


def test_get_view_state(base_parser: BaseParser, example_html: str) -> None:
    """Test that get_view_state retrieves the correct view state value."""
    view_state = base_parser.get_view_state(example_html)
    assert view_state == "state-value", "The view state value should be 'state-value'"


def test_get_view_state_not_found(base_parser: BaseParser, example_html: str) -> None:
    """Test that get_view_state raises an exception when the view state is not found."""
    html = "<html><body></body></html>"
    with pytest.raises(
        ElementNotFoundException, match="Element with ID '__VIEWSTATE' not found"
    ):
        base_parser.get_view_state(html)


def test_get_src_by_element_id(base_parser: BaseParser, example_html: str) -> None:
    """Test that get_src_by_element_id retrieves the correct src attribute."""
    src = base_parser.get_src_by_element_id(example_html, "imgEstado")

    assert (
        src == "../../Includes/images/FichaLight/iconos_estados/desierta.png"
    ), "The src attribute should be 'desierta.png'"


def test_get_src_by_element_id_not_found(
    base_parser: BaseParser, example_html: str
) -> None:
    """Test that get_src_by_element_id raises an exception when the element is not found."""
    with pytest.raises(
        ElementNotFoundException, match="Element with ID 'nonexistent' not found"
    ):
        base_parser.get_src_by_element_id(example_html, "nonexistent")


def test_get_src_by_element_id_no_src_attribute(base_parser: BaseParser) -> None:
    """Test that get_src_by_element_id raises an exception when the src attribute is not found."""
    html = "<html><body><img id='test'/></body></html>"
    with pytest.raises(IndexError):
        base_parser.get_src_by_element_id(html, "test")


def test_get_html_element_empty(base_parser: BaseParser) -> None:
    """Test that get_html_element raises an exception for empty HTML."""
    with pytest.raises(ValueError, match="Document is empty or invalid"):
        base_parser.get_html_element("")


def test_get_html_element_malformed(base_parser: BaseParser) -> None:
    """Test that get_html_element raises an exception when None is passed."""
    with pytest.raises(TypeError, match="expected string or bytes-like object"):
        base_parser.get_html_element(None)  # type: ignore[arg-type]


def test_get_on_click_by_element_id(base_parser: BaseParser, example_html: str) -> None:
    """Test that get_on_click_by_element_id retrieves the correct onclick attribute."""
    # HTML con un elemento que tiene el atributo `onclick`
    html = """
    <html>
        <body>
            <button id="btnTest" onclick="doSomething()">Click me</button>
        </body>
    </html>
    """
    onclick = base_parser.get_on_click_by_element_id(html, "btnTest")
    assert onclick == "doSomething()", "The onclick attribute should be 'doSomething()'"
