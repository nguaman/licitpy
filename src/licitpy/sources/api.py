from datetime import date


class API:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_monthly_tenders(self, start_date: date, end_date: date, limit: int = None):
        raise NotImplementedError("This method has not been implemented yet.")
