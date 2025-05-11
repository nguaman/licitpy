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


class ElementNotFoundException(Exception):
    """Exception raised when an HTML element is not found."""

    pass


class NonBusinessDayError(ValueError):
    """Raised when attempting to query for tenders on weekends or holidays."""

    pass


class InvalidTenderDataException(Exception):
    """
    Exception raised when Open Contracting Data Standard (OCDS) response data
    is missing required fields or has structural issues that prevent proper processing.
    """

    pass
