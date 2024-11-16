from datetime import timedelta
from typing import Optional


class Settings:
    def __init__(
        self,
        use_cache: bool = True,
        cache_expire_after: Optional[timedelta] = timedelta(hours=1),
        disable_progress_bar: bool = False,
    ):

        self.use_cache = use_cache
        self.cache_expire_after = cache_expire_after
        self.disable_progress_bar = disable_progress_bar


settings = Settings()
