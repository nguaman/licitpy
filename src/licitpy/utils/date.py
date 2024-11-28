from datetime import date


def convert_to_date(date_value: str | date) -> date:

    if isinstance(date_value, date):
        return date_value

    if isinstance(date_value, str):
        return date.fromisoformat(date_value)

    raise TypeError(f"Expected str or date, got {type(date_value)}")
