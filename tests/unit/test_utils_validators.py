import pytest

from licitpy.utils.validators import is_valid_public_market_code


def test_is_valid_public_market_code_valid_codes() -> None:
    """
    Test that the function returns True for valid public market codes.
    """
    valid_codes = [
        "6-51-O124",
        "48-77-LE24",
        "885-105-L124",
        "1658-1043-L124",
        "2513-2-LE24",
        "5060-452-L124",
        "750301-54-L124",
        "1375735-1-L124",
    ]
    for code in valid_codes:
        assert is_valid_public_market_code(code), f"Expected True for code {code}"


def test_is_valid_public_market_code_invalid_codes() -> None:
    """
    Test that the function returns False for invalid public market codes.
    """
    invalid_codes = [
        "6-51-0124",  # Invalid tier
        "48-77-LE2",  # Invalid format
        "885-105-L12",  # Invalid format
        "1658-1043-L12A",  # Invalid format
        "2513-2-LE240",  # Invalid format
        "5060-452-L12",  # Invalid format
        "750301-54-L12A",  # Invalid format
        "1375735-1-L12",  # Invalid format
    ]
    for code in invalid_codes:
        assert not is_valid_public_market_code(code), f"Expected False for code {code}"


def test_is_valid_public_market_code_none() -> None:
    """
    Test that the function raises a TypeError when the code is None.
    """
    with pytest.raises(
        TypeError, match="Invalid public market code: code cannot be None"
    ):
        is_valid_public_market_code(None)  # type: ignore[arg-type]


def test_is_valid_public_market_code_empty_string() -> None:
    """
    Test that the function raises a ValueError when the code is an empty string.
    """
    with pytest.raises(
        ValueError, match="Invalid public market code: code cannot be an empty string"
    ):
        is_valid_public_market_code("")


def test_is_valid_public_market_code_edge_cases() -> None:
    """
    Test that the function handles edge cases correctly.
    """
    edge_cases = [
        "1-1-L122",  # Minimum valid code
        "12345678-1234-L124",  # Maximum valid code
    ]
    for code in edge_cases:
        assert is_valid_public_market_code(code), f"Expected True for code {code}"
