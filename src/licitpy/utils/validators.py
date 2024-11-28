import re

from licitpy.types.tender.tender import Tier


def is_valid_public_market_code(code: str) -> bool:
    """
    Validates if the given code is a valid public market code.

    Args:
        code (str): The code to validate.

    Returns:
        bool: True if the code is valid, False otherwise.

    Raises:
        TypeError: If the code is None.
        ValueError: If the code is an empty string.
    """

    # Example of a valid code:
    # - 2513-2-LE24
    # - 750301-54-L124

    if code is None:
        raise TypeError("Invalid public market code: code cannot be None")

    if not code:
        raise ValueError("Invalid public market code: code cannot be an empty string")

    tier_pattern = "|".join([tier.value for tier in Tier])

    pattern = rf"^\d{{4,6}}-\d{{1,2}}-({tier_pattern})\d{{2}}$"
    return bool(re.match(pattern, code))
