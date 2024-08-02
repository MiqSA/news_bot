from src.settings import DEFAULT_MIN_RETRY_VALUE_INT
from src.interfaces.news import ScrapingNewsInterface
from src.logger import Log
from typing import Any


log_f = Log().main(__name__)


def apnews_pipeline(
    interface: ScrapingNewsInterface,
    variables: dict[str, Any],
    retries: int = DEFAULT_MIN_RETRY_VALUE_INT,
):
    """
    This pipeline get the more recent news on https://apnews.com/

    Steps:
    1. Open the site by following the link
    2. Enter a phrase in the search field
    3. On the result page if possible select a news category or section from the choose the latest (i.e., newest) news
    4. Get the values: title, date, and description.
    5. Store in an Excel file:
        - title
        - date
        - description (if available)
        - picture filename
        - count of search phrases in the title and description
        - True or False, depending on whether the title or description contains any amount of money. Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

    6. Download the news picture and specify the file name in the Excel file
    7.Follow steps 4-6 for all news that falls within the required time period
    """
    while retries>0:
        try:
            interface.run(variables)
            retries = 0
        except Exception as err:
            message_error = f"Error on execute news pipeline. It's only left {retries} retries."
            log_f.exception(message_error, exc_info=err)
            retries -=1
