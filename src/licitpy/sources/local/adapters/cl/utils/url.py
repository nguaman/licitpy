from pydantic import HttpUrl


def _build_lookup_tender_url(base_url: str, code: str) -> str:
    """Build the MercadoPublico URL for a tender."""
    return f"{base_url}?idlicitacion={code}"


def _build_url_from_redirect_header(base_url: str, location: str) -> HttpUrl:
    """Builds the final tender URL from the 'Location' header string."""
    query = location.split("qs=")[1].strip()

    url_str = f"{base_url}?qs={query}"

    return HttpUrl(url_str)
