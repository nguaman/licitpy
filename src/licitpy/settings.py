from datetime import timedelta


class Settings:
    def __init__(
        self,
        use_cache: bool = True,
        cache_expire_after: timedelta = timedelta(hours=1),
        disable_progress_bar: bool = False,
        output_dir: str = "/data/csv/",
    ):

        self.use_cache = use_cache
        self.cache_expire_after = cache_expire_after
        self.disable_progress_bar = disable_progress_bar
        self.output_dir = output_dir


settings = Settings()
