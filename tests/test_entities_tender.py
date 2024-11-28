import json
from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from licitpy.entities.tender import Tender
from licitpy.services.tender import TenderServices
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Region, Tier


@pytest.fixture
def mock_tender_services() -> TenderServices:

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
    mock_services.get_url.return_value = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2513-2-LE24"
    mock_services.get_html.return_value = "<html>Mock HTML</html>"
    mock_services.get_opening_date.return_value = date(2024, 11, 1)
    mock_services.get_closing_date.return_value = datetime(2024, 11, 30, 23, 59)
    mock_services.is_open.return_value = False
    mock_services.get_status.return_value = Status.UNSUCCESSFUL
    mock_services.get_title.return_value = (
        "Construcción y Reparación de Obras de Conservación"
    )
    mock_services.get_description.return_value = "Dichas obras de conservación mejorarán la captura de aguas lluvias, contribuirán a la resiliencia de los bosques nativos, y a las recargas de las napas freáticas en una superficie total a intervenir de 55 hectáreas, de las cuales se deben ejecutar un total de 2.948 metros lineales ML de construcción de OCAS, 890 ML de reparación de OCAS."
    mock_services.get_region.return_value = Region.V
    mock_services.get_tier.return_value = Tier.LE

    return mock_services


def test_tender_initialization_valid() -> None:
    """Test that Tender initializes correctly with valid data."""
    tender = Tender(
        code="2513-2-LE24",
        region=Region.RM,
        status=Status.PUBLISHED,
        title="Test Tender",
        description="This is a test tender.",
        opening_date=date(2024, 11, 1),
    )

    assert tender.code == "2513-2-LE24"
    assert tender.region == Region.RM
    assert tender.status == Status.PUBLISHED
    assert tender.title == "Test Tender"
    assert tender.description == "This is a test tender."
    assert tender.opening_date == date(2024, 11, 1)


def test_tender_initialization_code_empty() -> None:
    """Test Tender initialization with invalid data."""
    with pytest.raises(
        ValueError, match="Invalid public market code: code cannot be an empty string"
    ):
        Tender(code="", region=Region.RM)


def test_tender_initialization_with_code_none() -> None:
    with pytest.raises(
        TypeError, match="Invalid public market code: code cannot be None"
    ):
        Tender.create(code=None)  # type: ignore[arg-type]


def test_tender_properties_url(mock_tender_services: TenderServices) -> None:
    """Test that the url property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert (
        tender.url
        == "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2513-2-LE24"
    )


def test_tender_properties_html(mock_tender_services: TenderServices) -> None:
    """Test that the html property returns the correct value."""
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender.html == "<html>Mock HTML</html>"


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

    assert (
        tender.description
        == "Dichas obras de conservación mejorarán la captura de aguas lluvias, contribuirán a la resiliencia de los bosques nativos, y a las recargas de las napas freáticas en una superficie total a intervenir de 55 hectáreas, de las cuales se deben ejecutar un total de 2.948 metros lineales ML de construcción de OCAS, 890 ML de reparación de OCAS."
    )


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

    assert tender._ocds is None  # Initially not set

    ocds_data = tender.ocds  # Triggers lazy initialization

    assert (
        ocds_data.uri == "https://apis.mercadopublico.cl/OCDS/data/record/3955-54-LE24"
    )

    assert tender._ocds is ocds_data  # Now it should be set

    # Scenario 2: _ocds is already set, no re-initialization occurs
    mock_tender_services.get_ocds_data.reset_mock()  # Clear any previous calls to the mock
    ocds_data_second_access = tender.ocds  # Access the property again
    mock_tender_services.get_ocds_data.assert_not_called()  # Ensure the service is not called again

    assert ocds_data_second_access is ocds_data  # Confirm the same object is returned


def test_from_data() -> None:
    """Test the from_data class method."""
    tender = Tender.from_data(
        code="2513-2-LE24",
        region=Region.RM,
        status=Status.PUBLISHED,
        title="Test Title",
        description="Test Description",
        opening_date=datetime(2024, 11, 1),
    )

    assert tender.code == "2513-2-LE24"
    assert tender.region == Region.RM
    assert tender.status == Status.PUBLISHED
    assert tender.title == "Test Title"
    assert tender.description == "Test Description"
    assert tender.opening_date == datetime(2024, 11, 1)


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

    assert tender._url is None  # Initially not set

    url_data = tender.url  # Triggers lazy initialization

    assert (
        url_data
        == "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2513-2-LE24"
    )
    assert tender._url is url_data  # Now it should be set

    mock_tender_services.get_url.reset_mock()  # Clear any previous calls to the mock
    url_data_second_access = tender.url  # Access the property again
    mock_tender_services.get_url.assert_not_called()  # Ensure the service is not called again

    assert url_data_second_access is url_data  # Confirm the same object is returned


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
    assert tender._closing_date is None  # Initially not set

    closing_date = tender.closing_date  # Triggers lazy initialization

    assert closing_date == datetime(2024, 11, 30, 23, 59)
    assert tender._closing_date is closing_date  # Now it should be set

    mock_tender_services.get_closing_date.reset_mock()  # Clear any previous calls to the mock
    closing_date_second_access = tender.closing_date  # Access the property again
    mock_tender_services.get_closing_date.assert_not_called()  # Ensure the service is not called again

    assert (
        closing_date_second_access is closing_date
    )  # Confirm the same object is returned


def test_tier_property_initialization(mock_tender_services: TenderServices) -> None:
    """Test that the tier property initializes correctly.

    This test covers both scenarios of the conditional logic in the `tier` property:
    1. When `_tier` is initially `None`, it verifies that the `get_tier` service method is called
       and the returned value is correctly assigned to `_tier`.
    2. When `_tier` is already assigned, it verifies that `get_tier` is not called again, ensuring
       that the lazy initialization logic only executes once for this attribute.
    """
    tender = Tender(code="2513-2-LE24", services=mock_tender_services)

    assert tender._tier is None  # Initially not set

    tier_data = tender.tier  # Triggers lazy initialization

    assert tier_data == Tier.LE
    assert tender._tier is tier_data  # Now it should be set

    mock_tender_services.get_tier.reset_mock()  # Clear any previous calls to the mock
    tier_data_second_access = tender.tier  # Access the property again
    mock_tender_services.get_tier.assert_not_called()  # Ensure the service is not called again

    assert tier_data_second_access is tier_data  # Confirm the same object is returned
