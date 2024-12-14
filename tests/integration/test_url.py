import pytest
import requests


@pytest.mark.integration
def test_url_status() -> None:
    """
    Test that the URL for a tender returns status 200.
    """
    url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=kB7wNzIM1HVt0mPcG7xAGw=="
    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Expected status 200, got {response.status_code}"

@pytest.mark.integration
def test_url_api_ocds() -> None:
    """
    Test that the API (OCDS) URL for a tender returns status 200.
    """
    url = "https://apis.mercadopublico.cl/OCDS/data/tender/4326-1-LR24"

    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Expected status 200, got {response.status_code}"
