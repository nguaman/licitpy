from datetime import date, timedelta
from typing import Tuple, Union

from licitpy.types.search import TimeRange


def convert_to_date(date_value: str | date) -> date:

    if isinstance(date_value, date):
        return date_value

    if isinstance(date_value, str):
        return date.fromisoformat(date_value)

    raise TypeError(f"Expected str or date, got {type(date_value)}")


def _time_range(time_range: TimeRange) -> Tuple[date, date]:
    today = date.today()
    yesterday = today - timedelta(days=1)
    beginning_of_month = today.replace(day=1)

    if time_range == TimeRange.TODAY:
        return today, today
    elif time_range == TimeRange.FROM_YESTERDAY:
        return yesterday, yesterday
    elif time_range == TimeRange.THIS_MONTH:
        return beginning_of_month, today
    else:
        raise ValueError(f"Unsupported time range: {time_range}")


def determine_date_range(
    start_date: Union[str, date, None] = None,
    end_date: Union[str, date, None] = None,
    time_range: TimeRange = TimeRange.THIS_MONTH,
) -> Tuple[date, date]:

    if start_date is not None and end_date is not None:

        start_date = convert_to_date(start_date)
        end_date = convert_to_date(end_date)

        if end_date < start_date:
            raise ValueError("Start date cannot be greater than end date")

        return start_date, end_date

    return _time_range(time_range)
