from unittest.mock import MagicMock, Mock, patch

import pytest
from pydantic import HttpUrl

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.types.purchase_order import Status


@pytest.fixture
def mock_purchase_orders() -> list[Mock]:
    return [Mock(spec=PurchaseOrder) for _ in range(5)]


@pytest.fixture
def mock_services() -> MagicMock:
    return MagicMock(spec=PurchaseOrderServices)


@pytest.fixture
def purchase_order(mock_services: MagicMock) -> PurchaseOrder:
    return PurchaseOrder(code="750301-261-SE24", services=mock_services)


def test_purchase_order_url() -> None:
    test_code = "750301-261-SE24"

    expected_url = HttpUrl(
        "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    )

    with patch.object(
        PurchaseOrderServices, "get_url", return_value=expected_url
    ) as mock_get_url:
        purchase_order = PurchaseOrder(code=test_code, services=PurchaseOrderServices())

        result = purchase_order.url

        mock_get_url.assert_called_once_with(test_code)

        assert result == expected_url, f"Expected {expected_url}, got {result}"


def test_purchase_order_properties() -> None:

    mock_service = Mock()
    mock_service.get_url.return_value = "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    mock_service.get_html.return_value = "<html>Example</html>"
    mock_service.get_status.return_value = Status.ACCEPTED
    mock_service.get_title.return_value = "ORDEN DE COMPRA DESDE 750301-54-L124"

    purchase_order = PurchaseOrder(code="750301-261-SE24", services=mock_service)

    assert (
        purchase_order.url
        == "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    )
    assert purchase_order.html == "<html>Example</html>"
    assert purchase_order.status == Status.ACCEPTED
    assert purchase_order.title == "ORDEN DE COMPRA DESDE 750301-54-L124"

    mock_service.get_url.assert_called_once_with("750301-261-SE24")
    mock_service.get_html.assert_called_once_with(
        "https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=750301-261-SE24"
    )
    mock_service.get_status.assert_called_once_with("<html>Example</html>")
    mock_service.get_title.assert_called_once_with("<html>Example</html>")


def test_purchase_order_create() -> None:
    purchase_order = PurchaseOrder.create("750301-261-SE24")
    assert isinstance(purchase_order, PurchaseOrder)
    assert purchase_order.code == "750301-261-SE24"


def test_purchase_order_status() -> None:

    mock_service = Mock()
    mock_service.get_url.return_value = "http://example.com"
    mock_service.get_html.return_value = "<html>Example</html>"
    mock_service.get_status.return_value = Status.IN_PROCESS

    purchase_order = PurchaseOrder(code="750301-261-SE24", services=mock_service)

    assert purchase_order._status is None

    status = purchase_order.status

    assert status == Status.IN_PROCESS

    mock_service.get_url.assert_called_once_with("750301-261-SE24")
    mock_service.get_html.assert_called_once_with("http://example.com")
    mock_service.get_status.assert_called_once_with("<html>Example</html>")

    mock_service.reset_mock()

    status = purchase_order.status

    mock_service.get_url.assert_not_called()
    mock_service.get_html.assert_not_called()
    mock_service.get_status.assert_not_called()


def test_purchase_order_title() -> None:

    mock_service = Mock()
    mock_service.get_url.return_value = "http://example.com"
    mock_service.get_html.return_value = "<html>Example</html>"
    mock_service.get_title.return_value = "ORDEN DE COMPRA DESDE 750301-54-L124"

    purchase_order = PurchaseOrder(code="750301-261-SE24", services=mock_service)

    assert purchase_order._title is None

    title = purchase_order.title

    assert title == "ORDEN DE COMPRA DESDE 750301-54-L124"

    mock_service.get_url.assert_called_once_with("750301-261-SE24")
    mock_service.get_html.assert_called_once_with("http://example.com")
    mock_service.get_title.assert_called_once_with("<html>Example</html>")

    mock_service.reset_mock()

    title = purchase_order.title

    mock_service.get_url.assert_not_called()
    mock_service.get_html.assert_not_called()
    mock_service.get_title.assert_not_called()
