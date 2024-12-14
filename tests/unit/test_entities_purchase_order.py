from unittest.mock import MagicMock, Mock, patch

import pytest
from pydantic import HttpUrl
from pytest_mock import MockerFixture

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.types.purchase_order import Status


@pytest.fixture
def mock_purchase_orders() -> list[Mock]:
    return [Mock(spec=PurchaseOrder) for _ in range(5)]


@pytest.fixture
def mock_services() -> MagicMock:
    mock = MagicMock(spec=PurchaseOrderServices)

    url = "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    mock.get_url.return_value = url
    mock.get_html.return_value = "<html>Example</html>"
    mock.get_status.return_value = Status.ACCEPTED
    mock.get_title.return_value = "ORDEN DE COMPRA DESDE 750301-54-L124"

    return mock


@pytest.fixture
def purchase_order(mock_services: MagicMock) -> PurchaseOrder:
    return PurchaseOrder(code="750301-261-SE24", services=mock_services)


def test_purchase_order_url(
    mock_services: MagicMock, purchase_order: PurchaseOrder
) -> None:
    """Test the url property of the PurchaseOrder entity."""

    test_code = "750301-261-SE24"
    url = "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    expected_url = HttpUrl(url)

    # Mock the get_url method of the services object
    mock_services.get_url.return_value = expected_url

    # Get the url property of the purchase_order object
    result = purchase_order.url

    # Check that the get_url method was called with the test_code
    mock_services.get_url.assert_called_once_with(test_code)

    # Check that the result is the expected_url
    assert result == expected_url, f"Expected {expected_url}, got {result}"


def test_purchase_order_properties(
    mock_services: MagicMock, purchase_order: PurchaseOrder
) -> None:
    """Test the properties of the PurchaseOrder entity."""

    expected_url = "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    expected_html = "<html>Example</html>"
    expected_status = Status.ACCEPTED
    expected_title = "ORDEN DE COMPRA DESDE 750301-54-L124"

    assert purchase_order.url == expected_url, f"URL mismatch: {purchase_order.url}"
    assert purchase_order.html == expected_html, f"HTML mismatch: {purchase_order.html}"
    assert (
        purchase_order.status == expected_status
    ), f"Status mismatch: {purchase_order.status}"
    assert (
        purchase_order.title == expected_title
    ), f"Title mismatch: {purchase_order.title}"

    mock_services.get_url.assert_called_once_with("750301-261-SE24")
    mock_services.get_html.assert_called_once_with(expected_url)
    mock_services.get_status.assert_called_once_with(expected_html)
    mock_services.get_title.assert_called_once_with(expected_html)


def test_purchase_order_create() -> None:
    """Test the creation of a PurchaseOrder entity."""
    purchase_order = PurchaseOrder.create("750301-261-SE24")

    assert isinstance(purchase_order, PurchaseOrder)
    assert purchase_order.code == "750301-261-SE24"


def test_purchase_order_status_cached(
    mock_services: MagicMock, purchase_order: PurchaseOrder
) -> None:
    """Test that the status is cached and not retrieved again on subsequent calls."""

    purchase_order.status

    mock_services.reset_mock()

    purchase_order.status

    mock_services.get_url.assert_not_called()
    mock_services.get_html.assert_not_called()
    mock_services.get_status.assert_not_called()


def test_purchase_order_status_initial(
    mock_services: MagicMock, purchase_order: PurchaseOrder
) -> None:
    """Test that the status is retrieved correctly on the first call."""

    expected_html_content = "<html>Example</html>"
    expected_status = Status.ACCEPTED
    expected_url = "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    expected_code = "750301-261-SE24"

    assert purchase_order._status is None

    status = purchase_order.status

    assert status == expected_status

    mock_services.get_url.assert_called_once_with(expected_code)
    mock_services.get_html.assert_called_once_with(expected_url)
    mock_services.get_status.assert_called_once_with(expected_html_content)


def test_purchase_order_title_cached(
    mock_services: MagicMock, purchase_order: PurchaseOrder
) -> None:
    """Test that the title is cached and not retrieved again on subsequent calls."""

    purchase_order.title

    mock_services.reset_mock()

    purchase_order.title

    mock_services.get_url.assert_not_called()
    mock_services.get_html.assert_not_called()
    mock_services.get_title.assert_not_called()


def test_purchase_order_title_initial(
    mock_services: MagicMock, purchase_order: PurchaseOrder
) -> None:
    """Test that the title is retrieved correctly on the first call."""

    expected_html_content = "<html>Example</html>"
    expected_title = "ORDEN DE COMPRA DESDE 750301-54-L124"
    expected_url = "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    expected_code = "750301-261-SE24"

    assert purchase_order._title is None

    title = purchase_order.title

    assert title == expected_title

    mock_services.get_url.assert_called_once_with(expected_code)
    mock_services.get_html.assert_called_once_with(expected_url)
    mock_services.get_title.assert_called_once_with(expected_html_content)
