from datetime import date, timedelta
from typing import Optional, Union

from licitpy.entities.tenders import Tenders
from licitpy.settings import settings
from licitpy.sources import API, Local
from licitpy.types import TimeRange
from licitpy.utils.date import convert_to_date


class Licitpy:

    def __init__(
        self,
        api_key: Optional[str] = None,
        use_cache: Optional[bool] = settings.use_cache,
        expire_after: Optional[timedelta] = settings.cache_expire_after,
        disable_progress_bar: Optional[bool] = settings.disable_progress_bar,
    ):

        settings.use_cache = use_cache
        settings.cache_expire_after = expire_after
        settings.disable_progress_bar = disable_progress_bar

        self.licitpy = API(api_key=api_key) if api_key else Local()

    def from_date(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        time_range: Optional[TimeRange] = TimeRange.THIS_MONTH,
    ) -> Tenders:

        if not start_date and not end_date:

            today = date.today()
            yesterday = today - timedelta(days=1)
            beginning_of_month = today.replace(day=1)

            match time_range:
                case TimeRange.TODAY:
                    start_date, end_date = today, today
                case TimeRange.FROM_YESTERDAY:
                    start_date, end_date = yesterday, yesterday
                case TimeRange.THIS_MONTH:
                    start_date, end_date = beginning_of_month, today

        else:

            start_date = convert_to_date(start_date)
            end_date = convert_to_date(end_date)

            if end_date < start_date:
                raise ValueError("Start date cannot be greater than end date")

        return self.licitpy.get_monthly_tenders(start_date, end_date)
