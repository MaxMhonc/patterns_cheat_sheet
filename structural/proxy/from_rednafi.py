# https://rednafi.github.io/digressions/python/2020/06/16/python-proxy-pattern.html

import logging
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pprint import pprint

import httpx
from httpx._exceptions import ConnectTimeout, ReadTimeout
from functools import lru_cache

logging.basicConfig(level=logging.INFO)


class IFetchUrl(ABC):
    """Abstract base class. You can't instantiate this independently."""

    @abstractmethod
    def get_data(self, url: str) -> dict:
        pass

    @abstractmethod
    def get_headers(self, data: dict) -> dict:
        pass

    @abstractmethod
    def get_args(self, data: dict) -> dict:
        pass


class FetchUrl(IFetchUrl):
    """Concrete class that doesn't handle exceptions and loggings."""

    def get_data(self, url: str) -> dict:
        with httpx.Client() as client:
            response = client.get(url)
            data = response.json()
            return data

    def get_headers(self, data: dict) -> dict:
        return data["headers"]

    def get_args(self, data: dict) -> dict:
        return data["args"]


class ExcFetchUrl(IFetchUrl):
    """This class can be swapped out with the FetchUrl class.
    It provides additional exception handling and logging."""

    def __init__(self) -> None:
        self._fetch_url = FetchUrl()

    def get_data(self, url: str) -> dict:
        try:
            data = self._fetch_url.get_data(url)
            return data

        except ConnectTimeout:
            logging.error("Connection time out. Try again later.")
            sys.exit(1)

        except ReadTimeout:
            logging.error("Read timed out. Try again later.")
            sys.exit(1)

    def get_headers(self, data: dict) -> dict:
        headers = self._fetch_url.get_headers(data)
        logging.info(f"Getting the headers at {datetime.now()}")
        return headers

    def get_args(self, data: dict) -> dict:
        args = self._fetch_url.get_args(data)
        logging.info(f"Getting the args at {datetime.now()}")
        return args


class CacheFetchUrl(IFetchUrl):
    def __init__(self) -> None:
        self._fetch_url = ExcFetchUrl()

    @lru_cache(maxsize=32)
    def get_data(self, url: str) -> dict:
        data = self._fetch_url.get_data(url)
        return data

    def get_headers(self, data: dict) -> dict:
        headers = self._fetch_url.get_headers(data)
        return headers

    def get_args(self, data: dict) -> dict:
        args = self._fetch_url.get_args(data)
        return args


if __name__ == "__main__":

    # url = "https://postman-echo.com/get?foo1=bar_1&foo2=bar_2"

    fetch = CacheFetchUrl()
    for arg1, arg2 in zip([1, 2, 3, 1, 2, 3], [1, 2, 3, 1, 2, 3]):
        url = f"https://postman-echo.com/get?foo1=bar_{arg1}&foo2=bar_{arg2}"
        print(f"\n {'-' * 75}\n")
        data = fetch.get_data(url)
        print(f"Cache Info: {fetch.get_data.cache_info()}")
        pprint(fetch.get_headers(data))
        pprint(fetch.get_args(data))
