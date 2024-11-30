from unittest.mock import MagicMock, patch
from pydantic import HttpUrl
import pytest
from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.services.purchase_order import PurchaseOrderServices


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
