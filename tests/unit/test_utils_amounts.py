import pytest
from licitpy.utils.amounts import amount_to_int


# Test with a common amount value
def test_amount_to_int_with_valid_amount() -> None:
    assert amount_to_int("$ 7.613.726") == 7613726


# Test with extra spaces in the input string
def test_amount_to_int_with_extra_spaces() -> None:
    assert amount_to_int("  $ 7.613.726   ") == 7613726


# Test with a small amount value
def test_amount_to_int_with_small_amount() -> None:
    assert amount_to_int("$ 1.234") == 1234


# Test with a large amount value
def test_amount_to_int_with_large_amount() -> None:
    assert amount_to_int("$ 1.000.000.000") == 1000000000


# Test with a string that does not contain the currency symbol
def test_amount_to_int_without_currency_symbol() -> None:
    assert amount_to_int("7.613.726") == 7613726


# Test with an empty string, expecting a ValueError exception
def test_amount_to_int_with_empty_string() -> None:
    with pytest.raises(ValueError):
        amount_to_int("")


# Test with a string containing invalid characters, expecting a ValueError exception
def test_amount_to_int_with_invalid_characters() -> None:
    with pytest.raises(ValueError):
        amount_to_int("$ ABCD.EFG")


# Test with a negative amount value
def test_amount_to_int_with_negative_amount() -> None:
    assert amount_to_int("-$ 1.234") == -1234
