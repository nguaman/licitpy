import asyncio
import base64
import tempfile
import zipfile
from typing import List

import pandas
from pydantic import HttpUrl

from licitpy.core.downloader.adownloader import AsyncDownloader
from licitpy.core.downloader.downloader import SyncDownloader


class ChileanTenderAggregatorService:

    _API_BASE_URL = "https://api.mercadopublico.cl/APISOCDS/OCDS/listaOCDSAgnoMes"

    def __init__(self, downloader: SyncDownloader, adownloader: AsyncDownloader):
        """
        Initializes the ChileanTenderAggregatorService.

        Args:
            downloader: The synchronous HTTP downloader.
            adownloader: The asynchronous HTTP downloader.
        """
        self.downloader = downloader
        self.adownloader = adownloader

    def get_tenders_codes_from_api(self, year: int, month: int) -> list[str]:

        tenders: List[str] = []

        # Define the base URL for the API endpoint to fetch tender data
        base_url = self._API_BASE_URL

        # Format the URL for the first request, retrieving up to 1000 records
        url = f"{base_url}/{year}/{month:02d}/0/1000"

        # Perform the initial API request and parse the JSON response
        response = self.downloader.session.get(url)
        response.raise_for_status()

        # Parse the JSON response to extract tender records
        records = response.json()

        # Retrieve the total available records for the given month and year
        total = records["pagination"]["total"]

        # Extract tender codes from the first batch of data
        # "urlTender": "https://apis.mercadopublico.cl/OCDS/data/tender/2669-49-L125",

        tenders.extend(
            str(tender["urlTender"]).split("/")[-1] for tender in records["data"]
        )

        # Loop through additional records in blocks of 1000 to fetch the required amount
        for skip in range(1000, total, 1000):

            # Format the URL for subsequent requests, always fetching 1000 records per request
            url = f"{base_url}/{year}/{month:02d}/{skip}/1000"

            # Perform the API request and parse the JSON response
            response = self.downloader.session.get(url)
            response.raise_for_status()

            # Parse the JSON response to extract tender records
            records = response.json()

            tenders.extend(
                str(tender["urlTender"]).split("/")[-1] for tender in records["data"]
            )

        # Handle an API edge case:
        # Sometimes, 'urlTender' might be a base path without a specific tender ID,
        # Example:
        # {
        #   "ocid": "ocds-70d2nz-",
        #   "urlTender": "https://apis.mercadopublico.cl/OCDS/data/tender/",
        #   "urlAward": "https://apis.mercadopublico.cl/OCDS/data/award/"
        # }
        # Our method of splitting the URL by "/" and taking the last part
        # would result in an empty string for such cases.
        tenders = [tender for tender in tenders if tender != ""]

        # Return the exact number of requested records, sliced to the limit
        return tenders

    async def aget_tenders_codes_from_api(self, year: int, month: int) -> list[str]:

        tenders: List[str] = []

        # Define the base URL for the API endpoint to fetch tender data
        base_url = self._API_BASE_URL

        # Format the URL for the first request, retrieving up to 1000 records
        url = f"{base_url}/{year}/{month:02d}/0/1000"

        # Perform the initial API request and parse the JSON response
        # response = self.downloader.session.get(url)
        # response.raise_for_status()

        async with self.adownloader.session.get(url) as response:
            response.raise_for_status()

            # Parse the JSON response to extract tender records
            records = await response.json()

        # Retrieve the total available records for the given month and year
        total = records["pagination"]["total"]

        # Extract tender codes from the first batch of data
        # "urlTender": "https://apis.mercadopublico.cl/OCDS/data/tender/2669-49-L125",
        tenders.extend(
            str(tender["urlTender"]).split("/")[-1] for tender in records["data"]
        )

        urls = [
            f"{base_url}/{year}/{month:02d}/{skip}/1000"
            for skip in range(1000, total, 1000)
        ]

        records = await asyncio.gather(
            *[self.adownloader.session.get(url) for url in urls]
        )

        for record in records:
            record.raise_for_status()

            records = await record.json()

            tenders.extend(
                str(tender["urlTender"]).split("/")[-1] for tender in records["data"]
            )

        # Return the exact number of requested records, sliced to the limit
        return tenders

    def get_tenders_codes_from_csv(self, year: int, month: int) -> list[str]:

        tenders: List[str] = []

        url = HttpUrl(
            f"https://transparenciachc.blob.core.windows.net/lic-da/{year}-{month:01d}.zip"
        )

        content_base64 = self.downloader.download_file_to_base64(url)

        df: pandas.DataFrame

        with tempfile.NamedTemporaryFile(delete=True, suffix=".zip") as zip_file:

            zip_file.write(base64.b64decode(content_base64))
            zip_file.flush()

            with zipfile.ZipFile(zip_file.name, "r") as zip_ref:
                csv_file_name = zip_ref.namelist()[0]

                with zip_ref.open(csv_file_name) as csv_file:

                    df = pandas.read_csv(
                        csv_file, encoding="latin1", sep=";", usecols=["CodigoExterno"]
                    )

        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("No data found in the CSV file")

        # Drop duplicate records based on the 'code' column, keeping the first occurrence
        df = df.drop_duplicates(subset="CodigoExterno", keep="first")

        # Reset the index of the DataFrame after sorting
        df.reset_index(drop=True, inplace=True)

        # Remove empty strings from the 'code' column
        df = df[df["CodigoExterno"].str.strip() != ""]

        tenders.extend(
            tender["CodigoExterno"] for tender in df.to_dict(orient="records")
        )

        return tenders

    async def aget_tenders_codes_from_csv(self, year: int, month: int) -> list[str]:
        tenders: List[str] = []
        return tenders
