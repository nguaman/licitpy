from datetime import date, timedelta
from typing import Tuple, Union

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.settings import settings
from licitpy.sources import API, Local
from licitpy.types.search import TimeRange
from licitpy.utils.date import convert_to_date


class Licitpy:

    def __init__(
        self,
        api_key: str | None = None,
        use_cache: bool = settings.use_cache,
        expire_after: timedelta = settings.cache_expire_after,
        disable_progress_bar: bool = settings.disable_progress_bar,
    ):

        settings.use_cache = use_cache
        settings.cache_expire_after = expire_after
        settings.disable_progress_bar = disable_progress_bar

        self.licitpy: Union[API, Local] = API(api_key=api_key) if api_key else Local()

    def _time_range(
        self,
        time_range: TimeRange,
    ) -> Tuple[date, date]:

        today = date.today()
        yesterday = today - timedelta(days=1)
        beginning_of_month = today.replace(day=1)

        match time_range:
            case TimeRange.TODAY:
                return today, today
            case TimeRange.FROM_YESTERDAY:
                return yesterday, yesterday
            case TimeRange.THIS_MONTH:
                return beginning_of_month, today
            case _:
                raise ValueError(f"Unsupported time range: {time_range}")

    def _date_range(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        time_range: TimeRange = TimeRange.THIS_MONTH,
    ) -> Tuple[date, date]:

        if start_date is not None and end_date is not None:
            return convert_to_date(start_date), convert_to_date(end_date)

        return self._time_range(time_range)

    def from_date(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        time_range: TimeRange = TimeRange.THIS_MONTH,
    ) -> Tenders:

        start_date, end_date = self._date_range(start_date, end_date, time_range)

        if end_date < start_date:
            raise ValueError("Start date cannot be greater than end date")

        return self.licitpy.get_monthly_tenders(start_date, end_date)

    def from_code(self, code: str) -> Tender:
        return self.licitpy.get_tender(code)
