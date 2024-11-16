import base64
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from operator import itemgetter
from typing import Dict, List, Optional

import pandas
import requests
from pydantic import HttpUrl
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from tqdm import tqdm

from licitpy.downloader.base import BaseDownloader
from licitpy.parsers.tender import TenderParser
from licitpy.settings import settings


class TenderDownloader(BaseDownloader):

    def __init__(
        self,
        parser: Optional[TenderParser] = None,
    ) -> None:
        super().__init__()

        self.parser: TenderParser = parser or TenderParser()

    def get_tender_codes_from_api(
        self, year: int, month: int, skip: int = 0, limit: int = None
    ) -> List[str]:

        # Check if limit is set to 0 or a negative number; if so, return an empty list
        if limit is not None and limit <= 0:
            return []

        # Define the base URL for the API endpoint to fetch tender data
        base_url = "https://api.mercadopublico.cl/APISOCDS/OCDS/listaOCDSAgnoMes"

        # Format the URL for the first request, retrieving up to 1000 records
        url = f"{base_url}/{year}/{month:02}/{skip}/1000"

        # Perform the initial API request and parse the JSON response
        records = self.session.get(url).json()

        # Retrieve the total available records for the given month and year
        total = records["pagination"]["total"]

        # If limit is None, set it to total to fetch all available records
        if limit is None:
            limit = total

        # Extract tender codes from the first batch of data
        tenders = [
            {"CodigoExterno": str(tender["urlTender"]).split("/")[-1]}
            for tender in records["data"]
        ]

        # If the limit is within the first 1000 records, return the filtered tender list
        if limit <= 1000:
            return tenders[:limit]

        # Loop through additional records in blocks of 1000 to fetch the required amount
        for skip in range(1000, total, 1000):

            # If enough records are retrieved, exit the loop
            if len(tenders) >= limit:
                break

            # Format the URL for subsequent requests, always fetching 1000 records per request
            url = f"{base_url}/{year}/{month:02}/{skip}/1000"

            # Perform the API request and parse the JSON response
            records = self.session.get(url).json()

            # Append tender codes from the current batch to the tenders list
            tenders.extend(
                {"CodigoExterno": str(tender["urlTender"]).split("/")[-1]}
                for tender in records["data"]
            )

        # Return the exact number of requested records, sliced to the limit
        return tenders[:limit]

    def get_massive_tenders_csv_from_zip(
        self, year: int, month: int
    ) -> pandas.DataFrame:

        file_name = f"{year}-{month:01}.zip"

        response: requests.Response = self.session.get(
            f"https://transparenciachc.blob.core.windows.net/lic-da/{file_name}",
            timeout=(5, 30),
            stream=True,
        )

        file_size = int(response.headers.get("Content-Length", 0))

        content_base64 = self.download_file_base64(response, file_size, file_name)

        with tempfile.NamedTemporaryFile(delete=True, suffix=".zip") as zip_file:

            zip_file.write(base64.b64decode(content_base64))
            zip_file.flush()

            with zipfile.ZipFile(zip_file.name, "r") as zip_ref:
                csv_file_name = zip_ref.namelist()[0]

                with zip_ref.open(csv_file_name) as csv_file:

                    df = pandas.read_csv(
                        csv_file,
                        encoding="latin1",
                        sep=";",
                        usecols=["CodigoExterno", "FechaPublicacion", "RegionUnidad"],
                        parse_dates=["FechaPublicacion"],
                    )

        return df

    def get_tender_from_csv(
        self, year: int, month: int, limit: int = None
    ) -> List[Dict[str, str]]:

        df: pandas.DataFrame = self.get_massive_tenders_csv_from_zip(year, month)

        # Validate that each 'CodigoExterno' has a unique 'FechaPublicacion'
        if any(df.groupby("CodigoExterno")["FechaPublicacion"].nunique() > 1):
            raise ValueError("Inconsistent publication dates found")

        # Convert the 'FechaPublicacion' column to a date format
        df["FechaPublicacion"] = df["FechaPublicacion"].dt.date

        # Drop duplicate records based on the 'code' column, keeping the first occurrence
        df = df.drop_duplicates(subset="CodigoExterno", keep="first")

        # Sort the DataFrame by 'opening_date' in ascending order
        # The date is in the following format YYYY-MM-DD (ISO 8601)
        df = df.sort_values(by="FechaPublicacion", ascending=True)

        # Reset the index of the DataFrame after sorting
        df.reset_index(drop=True, inplace=True)

        # If limit is None, set it to the total number of records in the DataFrame
        if limit is None:
            limit = df.shape[0]

        tenders = df.to_dict(orient="records")

        return tenders[:limit]

    @retry(
        retry=retry_if_result(lambda r: "records" not in r),
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
    )
    def get_tender_ocds_data(self, code: str) -> dict:

        url = f"https://apis.mercadopublico.cl/OCDS/data/record/{code}"

        response = self.session.get(url)
        data = response.json()

        if "records" not in data:
            with self.session.cache_disabled():

                response = self.session.get(url)
                data = response.json()

                if "records" in data:
                    self.session.cache.save_response(response)

        return data

    def get_tender_publish_date_from_tender(self, tender_code: str) -> datetime:

        tender_data = self.get_tender_ocds_data(tender_code)
        return self.parser.get_tender_opening_date_from_tender_ocds_data(tender_data)

    def get_tender_codes(self, year: int, month: int) -> List[Dict[str, str]]:

        # It has no date, only the code: {'CodigoExterno': '3611-65-E224'}
        tenders_from_api = self.get_tender_codes_from_api(year, month)

        # From the CSV, we obtain the code, the publication date, and the region
        # {'CodigoExterno': '3938-63-L124','FechaPublicacion': '2024-11-02','RegionUnidad': 'Región de la Araucanía '}
        tenders_from_csv = self.get_tender_from_csv(year, month)

        csv_tender_codes = {tender["CodigoExterno"] for tender in tenders_from_csv}

        api_tenders_missing_date = [
            tender
            for tender in tenders_from_api
            if tender["CodigoExterno"] not in csv_tender_codes
        ]

        api_tenders_with_date: List[Dict[str, str]] = []

        with ThreadPoolExecutor(max_workers=16) as executor:

            futures = {
                executor.submit(
                    self.get_tender_publish_date_from_tender, tender["CodigoExterno"]
                ): tender
                for tender in api_tenders_missing_date
            }

            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=f"Fetching publication dates {year}-{month:02}",
                disable=settings.disable_progress_bar,
            ):

                tender_code = futures[future]["CodigoExterno"]

                publication_date = future.result()

                api_tenders_with_date.append(
                    {
                        "CodigoExterno": tender_code,
                        "FechaPublicacion": publication_date.date(),
                    }
                )

        tenders: List[Dict[str, str]] = tenders_from_csv + api_tenders_with_date
        tenders.sort(key=itemgetter("FechaPublicacion"))

        return tenders

    def get_tender_url_from_code(self, code: str) -> HttpUrl:

        base_url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"

        query = (
            self.session.head(f"{base_url}?idlicitacion={code}")
            .headers["Location"]
            .split("qs=")[1]
            .strip()
        )

        return HttpUrl(f"{base_url}?qs={query}")
