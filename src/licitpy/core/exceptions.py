class LicitpyError(Exception):
    """Base exception for all licitpy errors."""

    pass


class FetchError(LicitpyError):
    """Error during data fetching (network, HTTP error)."""

    pass


class ParsingError(LicitpyError):
    """Error during data parsing or mapping."""

    pass


class TenderNotFoundError(FetchError):
    """Specific error when a tender ID is not found."""

    pass


class UnsupportedCountryError(LicitpyError):
    """Error when a requested country code is not supported."""

    pass
