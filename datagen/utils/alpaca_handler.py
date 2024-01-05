import os
import requests

from datetime import datetime
from typing import List, Optional, Tuple
from dotenv import load_dotenv

from .logger import get_console_logger
from models import News


load_dotenv()

logger = get_console_logger()

try:
    ALPACA_API_KEY = os.environ["ALPACA_API_KEY"]
    ALPACA_API_SECRET = os.environ["ALPACA_API_SECRET"]
except KeyError:
    logger.error(
        "Please set the environment variables ALPACA_API_KEY and ALPACA_API_SECRET"
    )
    raise


def fetch_batch_of_news(
    from_date: datetime,
    to_date: datetime,
    page_token: Optional[str] = None,
) -> Tuple[List[News], str]:
    # prepare the request URL
    headers = {
        "Apca-Api-Key-Id": os.getenv("ALPACA_API_KEY"),
        "Apca-Api-Secret-Key": os.getenv("ALPACA_API_SECRET"),
    }
    params = {
        "start": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": to_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "limit": 50,
        "include_content": True,
        "sort": "ASC",
    }
    if page_token is not None:
        params["page_token"] = page_token

    url = "https://data.alpaca.markets/v1beta1/news"

    # ping API
    response = requests.get(url, headers=headers, params=params)

    # parse output
    list_of_news = []
    next_page_token = None

    if response.status_code == 200:  # Check if the request was successful
        # parse response into json
        news_json = response.json()

        # extract next page token (if any)
        next_page_token = news_json.get("next_page_token", None)

        for n in news_json["news"]:
            list_of_news.append(
                News(
                    headline=n["headline"],
                    date=n["updated_at"],
                    summary=n["summary"],
                    content=n["content"],
                )
            )
    else:
        logger.error("Request failed with status code:", response.status_code)

    return list_of_news, next_page_token


def download_historical_news(**kwargs) -> List:
    """
    Downloads historical news from Alpaca API
    """
    from_date = kwargs["from_date"]
    to_date = kwargs["to_date"]

    logger.info(f"Downloading historical news from {from_date} to {to_date}")
    list_of_news, next_page_token = fetch_batch_of_news(from_date, to_date)
    logger.info(f"Fetched {len(list_of_news)} news")
    logger.debug(f"Next page token: {next_page_token}")

    while next_page_token is not None:
        batch_of_news, next_page_token = fetch_batch_of_news(
            from_date, to_date, next_page_token
        )
        list_of_news += batch_of_news
        logger.info(f"Fetched a total of {len(list_of_news)} news")
        logger.debug(f"Next page token: {next_page_token}")

        logger.debug(f"Last date in batch: {batch_of_news[-1].date}")

    return list_of_news