from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.entities.tender import Tender
from licitpy.services.tender import TenderServices
from licitpy.types.attachments import Attachment
from licitpy.types.geography import Region
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Tier


@pytest.fixture
def mock_purchase_orders() -> MagicMock:
    return MagicMock(spec=PurchaseOrders)


@pytest.fixture
def mock_tender_services(mock_purchase_orders: MagicMock) -> TenderServices:

    mock_services = MagicMock(spec=TenderServices)

    mock_services.get_ocds_data.return_value = OpenContract(
        uri="https://apis.mercadopublico.cl/OCDS/data/record/3955-54-LE24",
        version="1.1",
        extensions=[],
        publisher={"name": "Dirección de Compras y Contratación Pública"},
        license="https://creativecommons.org/publicdomain/zero/1.0/",
        publishedDate="2024-10-14T10:08:27Z",
        records=[],
    )

    description = """
        Dichas obras de conservación mejorarán la captura de aguas lluvias, contribuirán a la resiliencia de los bosques nativos, 
        y a las recargas de las napas freáticas en una superficie total a intervenir de 55 hectáreas, 
        de las cuales se deben ejecutar un total de 2.948 metros lineales ML de construcción de OCAS, 
        890 ML de reparación de OCAS.
    """

    title = "Construcción y Reparación de Obras de Conservación"
    url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2513-2-LE24"
    html = """
        <html>Mock HTML</html>
    """

    mock_services.get_url.return_value = url
    mock_services.get_html.return_value = html
    mock_services.get_opening_date.return_value = date(2024, 11, 1)
    mock_services.get_closing_date.return_value = datetime(2024, 11, 30, 23, 59)
    mock_services.is_open.return_value = False
    mock_services.get_status.return_value = Status.UNSUCCESSFUL
    mock_services.get_title.return_value = title
    mock_services.get_description.return_value = description
    mock_services.get_region.return_value = Region.V
    mock_services.get_tier.return_value = Tier.LE

    mock_services.get_attachment_url.return_value = "https://example.com/attachment"
    mock_services.get_attachments_from_url.return_value = []
    mock_services.get_tender_purchase_orders.return_value = mock_purchase_orders

    mock_services.get_signed_base_from_attachments.return_value = Attachment(
        name="Bases_750301-54-L124.pdf",
        description="Archivo firmado",
        type="Anexo Resolucion Electronica (Firmada)",
        id="123",
        url="https://example.com/signed_base.pdf",
        content_type="application/pdf",
        size=123456,
        upload_date="2024-12-14",
        file_type="pdf",
    )

    return mock_services


def test_tender_initialization_valid() -> None:
    """Test that Tender initializes correctly with valid data."""
    tender = Tender(
        code="2513-2-LE24",
        region=Region.RM,
        status=Status.PUBLISHED,
        title="Test Tender",
        description="This is a test tender.",
        opening_date=datetime(2024, 11, 1, 0, 0),
    )

    assert tender.code == "2513-2-LE24"
    assert tender.region == Region.RM
    assert tender.status == Status.PUBLISHED
    assert tender.title == "Test Tender"
    assert tender.description == "This is a test tender."
    assert tender.opening_date == datetime(2024, 11, 1, 0, 0)


def test_tender_initialization_code_empty() -> None:
    """Test Tender initialization with invalid data."""
    with pytest.raises(
        ValueError, match="Invalid public market code: code cannot be an empty string"
    ):
        Tender(code="", region=Region.RM)


def test_tender_properties_url(mock_tender_services: TenderServices) -> None:
    """Test that the url property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)
    url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2513-2-LE24"

    assert tender.url == url


def test_tender_properties_html(mock_tender_services: TenderServices) -> None:
    """Test that the html property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    html = """
        <html>Mock HTML</html>
    """

    assert tender.html == html


def test_tender_properties_opening_date(mock_tender_services: TenderServices) -> None:
    """Test that the opening_date property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.opening_date == date(2024, 11, 1)


def test_tender_properties_closing_date(mock_tender_services: TenderServices) -> None:
    """Test that the closing_date property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)
    assert tender.closing_date == datetime(2024, 11, 30, 23, 59)


def test_tender_is_open(mock_tender_services: TenderServices) -> None:
    """Test that the is_open property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.is_open is False


def test_tender_properties_status(mock_tender_services: TenderServices) -> None:
    """Test that the status property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.status == Status.UNSUCCESSFUL


def test_tender_properties_title(mock_tender_services: TenderServices) -> None:
    """Test that the title property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.title == "Construcción y Reparación de Obras de Conservación"


def test_tender_properties_description(mock_tender_services: TenderServices) -> None:
    """Test that the description property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    description = """
        Dichas obras de conservación mejorarán la captura de aguas lluvias, contribuirán a la resiliencia de los bosques nativos, 
        y a las recargas de las napas freáticas en una superficie total a intervenir de 55 hectáreas, 
        de las cuales se deben ejecutar un total de 2.948 metros lineales ML de construcción de OCAS, 
        890 ML de reparación de OCAS.
    """

    assert tender.description == description


def test_tender_properties_region(mock_tender_services: TenderServices) -> None:
    """Test that the region property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.region == Region.V


def test_tender_properties_tier(mock_tender_services: TenderServices) -> None:
    """Test that the tier property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.tier == Tier.LE


def test_tender_services_not_initialized() -> None:
    """Test the fallback when services are not provided."""
    tender = Tender(code="2513-2-LE24")

    assert tender.services is not None


def test_tender_default_properties() -> None:
    """Test the default values of the Tender properties."""
    tender = Tender(code="2513-2-LE24")

    assert tender._html is None
    assert tender._ocds is None
    assert tender._url is None
    assert tender._status is None
    assert tender._title is None
    assert tender._opening_date is None
    assert tender._closing_date is None
    assert tender._description is None
    assert tender._region is None
    assert tender._tier is None


def test_tender_property_setters() -> None:
    """Test the manual setting of properties if needed."""

    tender = Tender(code="2513-2-LE24")
    tender._html = "<html>Test HTML</html>"
    tender._status = Status.PUBLISHED
    tender._title = "Set Title"
    tender._description = "Set Description"

    assert tender.html == "<html>Test HTML</html>"
    assert tender.status == Status.PUBLISHED
    assert tender.title == "Set Title"
    assert tender.description == "Set Description"


def test_invalid_public_market_code() -> None:
    """Test initialization with an invalid public market code."""
    with pytest.raises(ValueError, match="Invalid public market code: invalid_code"):
        Tender(code="invalid_code")


def test_ocds_property_initialization(mock_tender_services: TenderServices) -> None:
    """Test that the ocds property initializes correctly.

    This test covers both scenarios of the conditional logic in the `ocds` property:
    1. When `_ocds` is initially `None`, it verifies that the `get_ocds_data` service method is called
    and the returned value is correctly assigned to `_ocds`.
    2. When `_ocds` is already assigned, it verifies that `get_ocds_data` is not called again, ensuring
    that the lazy initialization logic only executes once for this attribute.
    """
    # Scenario 1: _ocds is None and should be initialized
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    # Initially not set
    assert tender._ocds is None

    # Triggers lazy initialization
    ocds_data = tender.ocds

    assert (
        ocds_data.uri == "https://apis.mercadopublico.cl/OCDS/data/record/3955-54-LE24"
    )

    # Now it should be set
    assert tender._ocds is ocds_data

    # Scenario 2: _ocds is already set, no re-initialization occurs

    # Clear any previous calls to the mock
    mock_tender_services.get_ocds_data.reset_mock()

    # Access the property again
    ocds_data_second_access = tender.ocds

    # Ensure the service is not called again
    mock_tender_services.get_ocds_data.assert_not_called()

    # Confirm the same object is returned
    assert ocds_data_second_access is ocds_data


def test_tender_default_services() -> None:
    """Test default initialization of services."""
    tender = Tender(code="2513-2-LE24")
    assert tender.services is not None
    assert tender.services.__class__.__name__ == "TenderServices"


def test_url_property_initialization(mock_tender_services: TenderServices) -> None:
    """Test that the url property initializes correctly.

    This test covers both scenarios of the conditional logic in the `url` property:
    1. When `_url` is initially `None`, it verifies that the `get_url` service method is called
    and the returned value is correctly assigned to `_url`.
    2. When `_url` is already assigned, it verifies that `get_url` is not called again, ensuring
    that the lazy initialization logic only executes once for this attribute.
    """
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    # Initially not set
    assert tender._url is None

    # Triggers lazy initialization
    url_data = tender.url

    url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2513-2-LE24"
    assert url_data == url

    # Now it should be set
    assert tender._url is url_data

    # Clear any previous calls to the mock
    mock_tender_services.get_url.reset_mock()

    # Access the property again
    url_data_second_access = tender.url

    # Ensure the service is not called again
    mock_tender_services.get_url.assert_not_called()

    # Confirm the same object is returned
    assert url_data_second_access is url_data


def test_closing_date_property_initialization(
    mock_tender_services: TenderServices,
) -> None:
    """Test that the closing_date property initializes correctly.

    This test covers both scenarios of the conditional logic in the `closing_date` property:
    1. When `_closing_date` is initially `None`, it verifies that the `get_closing_date` service method is called
    and the returned value is correctly assigned to `_closing_date`.
    2. When `_closing_date` is already assigned, it verifies that `get_closing_date` is not called again, ensuring
    that the lazy initialization logic only executes once for this attribute.
    """

    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    # Initially not set
    assert tender._closing_date is None

    # Triggers lazy initialization
    closing_date = tender.closing_date

    assert closing_date == datetime(2024, 11, 30, 23, 59)

    # Now it should be set
    assert tender._closing_date is closing_date

    # Clear any previous calls to the mock
    mock_tender_services.get_closing_date.reset_mock()

    # Access the property again
    closing_date_second_access = tender.closing_date

    # Ensure the service is not called again
    mock_tender_services.get_closing_date.assert_not_called()

    # Confirm the same object is returned
    assert closing_date_second_access is closing_date


def test_tier_property_initialization(mock_tender_services: TenderServices) -> None:
    """Test that the tier property initializes correctly.

    This test covers both scenarios of the conditional logic in the `tier` property:
    1. When `_tier` is initially `None`, it verifies that the `get_tier` service method is called
    and the returned value is correctly assigned to `_tier`.
    2. When `_tier` is already assigned, it verifies that `get_tier` is not called again, ensuring
    that the lazy initialization logic only executes once for this attribute.
    """
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    # Initially not set
    assert tender._tier is None

    # Triggers lazy initialization
    tier_data = tender.tier

    assert tier_data == Tier.LE

    # Now it should be set
    assert tender._tier is tier_data

    # Clear any previous calls to the mock
    mock_tender_services.get_tier.reset_mock()

    # Access the property again
    tier_data_second_access = tender.tier

    # Ensure the service is not called again
    mock_tender_services.get_tier.assert_not_called()

    # Confirm the same object is returned
    assert tier_data_second_access is tier_data


def test_tender_attachment_url_property_initialization(
    mock_tender_services: MagicMock,
) -> None:
    """Test that the attachment_url property initializes correctly and is cached."""

    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender._attachment_url is None

    attachment_url = tender.attachment_url

    assert attachment_url == "https://example.com/attachment"
    assert tender._attachment_url == attachment_url

    mock_tender_services.get_attachment_url.reset_mock()

    attachment_url_again = tender.attachment_url
    mock_tender_services.get_attachment_url.assert_not_called()

    assert attachment_url_again == attachment_url


def test_tender_attachments_property_initialization(
    mock_tender_services: MagicMock,
) -> None:
    """Test that the attachments property initializes correctly and is cached."""

    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender._attachments is None

    attachments = tender.attachments

    assert attachments == []
    assert tender._attachments == attachments

    mock_tender_services.get_attachments_from_url.reset_mock()

    attachments_again = tender.attachments
    mock_tender_services.get_attachments_from_url.assert_not_called()

    assert attachments_again == attachments


def test_tender_purchase_orders_property_initialization(
    mock_tender_services: MagicMock,
) -> None:
    """Test that the purchase_orders property initializes correctly and is cached."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender._purchase_orders is None

    purchase_orders = tender.purchase_orders
    assert purchase_orders is not None
    assert tender._purchase_orders == purchase_orders

    mock_tender_services.get_tender_purchase_orders.reset_mock()

    purchase_orders_again = tender.purchase_orders
    mock_tender_services.get_tender_purchase_orders.assert_not_called()
    assert purchase_orders_again == purchase_orders


def test_tender_signed_base_property_initialization(
    mock_tender_services: MagicMock,
) -> None:
    """Test that the signed_base property initializes correctly and is cached."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender._signed_base is None

    signed_base = tender.signed_base

    assert signed_base is not None
    assert tender._signed_base == signed_base

    mock_tender_services.get_signed_base_from_attachments.reset_mock()

    signed_base_again = tender.signed_base
    mock_tender_services.get_signed_base_from_attachments.assert_not_called()

    assert signed_base_again == signed_base
