import pytest
from lxml.html import HtmlElement

from licitpy.parsers.attachment import AttachmentParser
from licitpy.types.attachments import Attachment, FileType


@pytest.fixture
def attachment_parser() -> AttachmentParser:
    return AttachmentParser()


def test_get_table_attachments(attachment_parser: AttachmentParser) -> None:
    html = """
    <html>
        <body>
            <table id="DWNL_grdId">
                <tr><td>Sample Row</td></tr>
            </table>
        </body>
    </html>
    """
    table = attachment_parser._get_table_attachments(html)
    assert table.tag == "table", "The tag of the returned element should be 'table'"


def test_get_table_attachments_not_found(attachment_parser: AttachmentParser) -> None:
    html = "<html><body></body></html>"
    with pytest.raises(ValueError, match="Table with ID 'DWNL_grdId' not found"):
        attachment_parser._get_table_attachments(html)


def test_get_table_attachments_rows(attachment_parser: AttachmentParser) -> None:
    html = """
    <table>
        <tr class="row"><td>Row 1</td></tr>
        <tr class="row"><td>Row 2</td></tr>
    </table>
    """
    table = attachment_parser.get_html_element(html)
    rows = attachment_parser._get_table_attachments_rows(table)
    assert len(rows) == 2, "The number of rows should be 2"


def test_parse_size_attachment(attachment_parser: AttachmentParser) -> None:
    html = "<td><span>1024 Kb</span></td>"
    element = attachment_parser.get_html_element(html)
    size = attachment_parser._parse_size_attachment(element)
    assert size == 1024 * 1024, "The parsed size should be 1 MB in bytes"


def test_extract_attachment_id(attachment_parser: AttachmentParser) -> None:
    html = '<td><input id="ctl123" /></td>'
    element = attachment_parser.get_html_element(html)
    attachment_id = attachment_parser._extract_attachment_id(element)
    assert attachment_id == "123", "The extracted attachment ID should be '123'"


def test_extract_content_from_attachment_row(
    attachment_parser: AttachmentParser,
) -> None:
    html = "<td><span>Attachment Content</span></td>"
    element = attachment_parser.get_html_element(html)
    content = attachment_parser._extract_content_from_attachment_row(element)
    assert content == "Attachment Content", "The extracted content should match"


def test_get_table_attachments_rows_valid(attachment_parser: AttachmentParser) -> None:
    html = """
    <table>
        <tr class="row1"><td>Row 1</td></tr>
        <tr class="row2"><td>Row 2</td></tr>
        <tr class="row3"><td>Row 3</td></tr>
    </table>
    """
    table: HtmlElement = attachment_parser.get_html_element(html)

    # Call the function
    rows = attachment_parser._get_table_attachments_rows(table)

    # Assert that the correct number of rows is returned
    assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"

    # Optionally, validate the content of rows
    row_texts = [row.xpath("td/text()")[0] for row in rows]
    expected_texts = ["Row 1", "Row 2", "Row 3"]

    assert row_texts == expected_texts, f"Expected {expected_texts}, got {row_texts}"


def test_get_table_attachments_rows_no_rows(
    attachment_parser: AttachmentParser,
) -> None:
    html = """
    <table>
        <!-- No rows with a class -->
    </table>
    """
    table: HtmlElement = attachment_parser.get_html_element(html)

    # Call the function and expect an exception
    with pytest.raises(ValueError, match="No rows found in the table"):
        attachment_parser._get_table_attachments_rows(table)


def test_parse_size_attachment_success(attachment_parser: AttachmentParser) -> None:
    """
    Test that `_parse_size_attachment` correctly parses valid size values.
    """
    html = "<td><span>1024 Kb</span></td>"
    td_element = attachment_parser.get_html_element(html)
    result = attachment_parser._parse_size_attachment(td_element)
    expected_size = 1024 * 1024  # 1 MB in bytes
    assert result == expected_size, f"Expected {expected_size}, got {result}"


def test_parse_size_attachment_invalid_format(
    attachment_parser: AttachmentParser,
) -> None:
    """
    Test that `_parse_size_attachment` raises a ValueError for invalid size formats.
    """
    html = "<td><span>invalid_size</span></td>"
    td_element = attachment_parser.get_html_element(html)
    with pytest.raises(ValueError, match="Invalid size format: invalid_size"):
        attachment_parser._parse_size_attachment(td_element)


def test_parse_size_attachment_missing_size(
    attachment_parser: AttachmentParser,
) -> None:
    """
    Test that `_parse_size_attachment` raises an IndexError when size text is missing.
    """
    html = "<td></td>"
    td_element = attachment_parser.get_html_element(html)
    with pytest.raises(IndexError, match="list index out of range"):
        attachment_parser._parse_size_attachment(td_element)


def test_extract_attachment_id_no_input_id(attachment_parser: AttachmentParser) -> None:
    """
    Test that `_extract_attachment_id` raises a ValueError when no input ID is found.
    """
    html = "<td></td>"  # No input element present
    td_element = attachment_parser.get_html_element(html)

    with pytest.raises(ValueError, match="No input ID found in the first column"):
        attachment_parser._extract_attachment_id(td_element)


def test_extract_attachment_id_no_match(attachment_parser: AttachmentParser) -> None:
    """
    Test that `_extract_attachment_id` raises a ValueError when the input ID does not match the regex.
    """
    html = '<td><input id="invalid123" /></td>'
    element = attachment_parser.get_html_element(html)

    with pytest.raises(ValueError, match="No match found for attachment ID"):
        attachment_parser._extract_attachment_id(element)


def test_extract_content_from_attachment_row_valid(
    attachment_parser: AttachmentParser,
) -> None:
    """
    Test that `_extract_content_from_attachment_row` extracts the text content from a valid td element.
    """
    html = "<td><span>Attachment Content</span></td>"
    element = attachment_parser.get_html_element(html)

    result = attachment_parser._extract_content_from_attachment_row(element)
    expected_content = "Attachment Content"
    assert result == expected_content, f"Expected '{expected_content}', got '{result}'"


def test_extract_content_from_attachment_row_no_content(
    attachment_parser: AttachmentParser,
) -> None:
    """
    Test that `_extract_content_from_attachment_row` returns None when there is no text content in the td element.
    """
    html = "<td><span></span></td>"  # Empty span element
    element = attachment_parser.get_html_element(html)

    result = attachment_parser._extract_content_from_attachment_row(element)
    assert result is None, "Expected None when the span has no text content"


def test_extract_content_from_attachment_row_missing_span(
    attachment_parser: AttachmentParser,
) -> None:
    """
    Test that `_extract_content_from_attachment_row` returns None when there is no span element in the td.
    """
    html = "<td></td>"  # No span element
    element = attachment_parser.get_html_element(html)

    result = attachment_parser._extract_content_from_attachment_row(element)
    assert result is None, "Expected None when no span element is present in the td"


def test_get_attachments_valid(attachment_parser: AttachmentParser) -> None:
    """
    Test that `get_attachments` correctly extracts a list of attachments from a valid HTML table.
    """
    html = """
    <html>
        <table id="DWNL_grdId">
            <tr class="row">
                <td><input id="ctl123" /></td>
                <td><span>Attachment1.pdf</span></td>
                <td><span>Type1</span></td>
                <td><span>Description1</span></td>
                <td><span>1024 Kb</span></td>
                <td><span>2024-12-10</span></td>
            </tr>
            <tr class="row">
                <td><input id="ctl124" /></td>
                <td><span>Attachment2.docx</span></td>
                <td><span>Type2</span></td>
                <td><span>Description2</span></td>
                <td><span>2048 Kb</span></td>
                <td><span>2024-12-11</span></td>
            </tr>
        </table>
    </html>
    """
    result = attachment_parser.get_attachments(html)

    expected_attachments = [
        Attachment(
            id="123",
            name="Attachment1.pdf",
            type="Type1",
            description="Description1",
            size=1024 * 1024,
            upload_date="2024-12-10",
            file_type=FileType.PDF,
        ),
        Attachment(
            id="124",
            name="Attachment2.docx",
            type="Type2",
            description="Description2",
            size=2048 * 1024,
            upload_date="2024-12-11",
            file_type=FileType.DOCX,
        ),
    ]

    assert (
        result == expected_attachments
    ), f"Expected {expected_attachments}, got {result}"


def test_get_attachments_missing_name(attachment_parser: AttachmentParser) -> None:
    """
    Test that `get_attachments` raises a ValueError when an attachment name is missing.
    """
    html = """
    <html>
        <table id="DWNL_grdId">
            <tr class="row">
                <td><input id="ctl123" /></td>
                <td><span></span></td> <!-- Name missing -->
                <td><span>Type1</span></td>
                <td><span>Description1</span></td>
                <td><span>1024 Kb</span></td>
                <td><span>2024-12-10</span></td>
            </tr>
        </table>
    </html>
    """
    with pytest.raises(ValueError, match="Attachment name not found"):
        attachment_parser.get_attachments(html)


def test_get_attachments_invalid_size(attachment_parser: AttachmentParser) -> None:
    """
    Test that `get_attachments` raises a ValueError when the size format is invalid.
    """
    html = """
    <html>
        <table id="DWNL_grdId">
            <tr class="row">
                <td><input id="ctl123" /></td>
                <td><span>Attachment1.pdf</span></td>
                <td><span>Type1</span></td>
                <td><span>Description1</span></td>
                <td><span>invalid_size</span></td> <!-- Invalid size -->
                <td><span>2024-12-10</span></td>
            </tr>
        </table>
    </html>
    """
    with pytest.raises(ValueError, match="Invalid size format: invalid_size"):
        attachment_parser.get_attachments(html)


def test_get_attachments_no_input_id(attachment_parser: AttachmentParser) -> None:
    """
    Test that `get_attachments` raises a ValueError when an input ID is missing.
    """
    html = """
    <html>
        <table id="DWNL_grdId">
            <tr class="row">
                <td></td> <!-- Missing input ID -->
                <td><span>Attachment1.pdf</span></td>
                <td><span>Type1</span></td>
                <td><span>Description1</span></td>
                <td><span>1024 Kb</span></td>
                <td><span>2024-12-10</span></td>
            </tr>
        </table>
    </html>
    """
    with pytest.raises(ValueError, match="No input ID found in the first column"):
        attachment_parser.get_attachments(html)


def test_get_attachments_no_table(attachment_parser: AttachmentParser) -> None:
    """
    Test that `get_attachments` raises a ValueError when the attachments table is missing.
    """
    html = """
    <html>
        <body></body> <!-- No table -->
    </html>
    """
    with pytest.raises(ValueError, match="Table with ID 'DWNL_grdId' not found"):
        attachment_parser.get_attachments(html)
