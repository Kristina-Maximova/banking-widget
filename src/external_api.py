import datetime
import os
from typing import Any

import requests
import requests.exceptions
from dotenv import load_dotenv

from src.my_logging import external_api_logger

load_dotenv()
API_key_currency = os.getenv("API_key_currency")
API_key_shares = os.getenv("API_key_shares")
api_ = os.getenv("api_")

url = "https://api.apilayer.com/exchangerates_data/convert"
# в этом api квота 25 запросов в день, данные на конкретный исторический день:
url_second = "https://www.alphavantage.co/query"
# для тестовых прогонов:
url_ = "https://financialmodelingprep.com/api/v3/stock/list"


def get_currency_rate(date_: str, currency: str = "USD") -> float | Any:
    """Функция, возвращающая курс валюты на указанную дату
    первым аргументом принимает строку с датой в формате YYYY-MM-DD,
    вторым аргументом - код валюты, по-умолчанию "USD" """
    try:
        payload = {
            "amount": "1",
            "from": f"{currency}",
            "to": "RUB",
            "date": f"{date_}"
        }
        headers = {
            "apikey": f"{API_key_currency}"
        }
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            if result:
                external_api_logger.info("Курсы валют успешно получены")
                return round(result["result"], 2)
            else:
                return float(0)
        else:
            external_api_logger.warning(f"Ошибка запроса на курс валют {response.status_code}")
            return float(0)
    except requests.exceptions.RequestException as e:
        external_api_logger.warning(f"Ошибка: {e}")
        return float(0)


def get_stock_price(date_line: str, stock_name: str) -> str | Any:
    """ Функция принимает строку с датой формата YYYY-MM-DD HH:MM:SS и название акции,
    возвращает среднюю за месяц стоимость акции в формате строки"""
    # за некоторые дни нет данных на сайте
    try:
        date_obj = datetime.datetime.strptime(date_line, "%Y-%m-%d %H:%M:%S")
        date_as_key = date_obj.strftime("%Y-%m-%d")
        month = date_obj.strftime("%Y-%m")

        try:
            payload = {
                "function": "MIDPRICE",
                "symbol": f"{stock_name}",
                "interval": "daily",
                "month": f"{month}",
                "time_period": "30",
                "apikey": f"{API_key_shares}"
            }
            response = requests.get(f"{url_second}", params=payload)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()

                new_result = result["Technical Analysis: MIDPRICE"][f"{date_as_key}"]["MIDPRICE"]
                external_api_logger.info("Получен прайс по акциям")
                return new_result
            else:
                return ""
                external_api_logger.warning(f"Ошибка запроса: {response.status_code}")

        except requests.exceptions.RequestException as e:
            external_api_logger.warning(f"Ошибка {e}")
            return ""
    except ValueError as e:
        external_api_logger.warning(f"Нет даты для получения курса валюты, ошибка {e}")
        return ""


# для тестовых прогонов:
def get_stock_price_1(stock_name: str) -> float | Any:
    try:
        payload = {"apikey": f"{api_}"}
        response = requests.get(f"{url_}", params=payload)
        result = response.json()
        status_code = response.status_code
        if status_code == 200:
            for elem in result:
                if elem["symbol"] == stock_name:
                    price = round(elem["price"], 2)
                else:
                    continue
            if price:
                external_api_logger.info("Получен прайс по акциям")
                return price
            else:
                return float(0)
        else:
            return float(0)
            external_api_logger.warning(f"Ошибка stock_price_1, status_code: {response.status_code}")
    except Exception as e:
        external_api_logger.warning(f"Ошибка{e}")
        return float(0)

# if __name__ == "__main__":
# user_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#
# my_date = "2023-01-19 05:44:00"
#
# a = get_stock_price_1("AMZN")
# print(a)
