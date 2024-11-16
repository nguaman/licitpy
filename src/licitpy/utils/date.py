from datetime import date
from typing import Optional, Union


def convert_to_date(date_value: Union[str, date]) -> Optional[date]:
    return date.fromisoformat(date_value) if isinstance(date_value, str) else date_value
