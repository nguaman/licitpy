from enum import Enum


class Country(Enum):
    """
    Supported countries for procurement data.
    The value represents the country code used in configurations and URLs.
    """

    CL = "cl"  # Chile
    EU = "eu"  # European Union
