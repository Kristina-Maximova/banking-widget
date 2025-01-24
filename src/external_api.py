import os

import requests
import requests.exceptions
from dotenv import load_dotenv
from src.utils import get_date, get_month, get_early_date
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


def get_currency_rate(date_: str, currency: str = "USD") -> float:
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


def get_stock_price(date_line: str, stock_name: str) -> str:
    """ Функция принимает строку с датой формата YYYY-MM-DD HH:MM:SS и название акции,
    возвращает среднюю за месяц стоимость акции в формате строки"""
    # за некоторые дни нет данных на сайте
    date = get_date(date_line)
    month = get_month(date_line)
    early_date = get_early_date(date)
    if date != "" and month != "":
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
                if  f"{date}" in result['Technical Analysis: MIDPRICE']:
                    new_result = result['Technical Analysis: MIDPRICE'][f"{date}"]['MIDPRICE']
                    external_api_logger.info("Получен прайс по акциям")
                    return new_result
                elif f"{early_date}" in result['Technical Analysis: MIDPRICE']:
                    new_result = result['Technical Analysis: MIDPRICE'][f"{early_date}"]['MIDPRICE']
                    external_api_logger.info("Получен прайс по акциям")
                    return new_result
                else:
                    external_api_logger.warning("Нет данных по акциям на эту дату или израсходована квота запросов")
                    return "" # можно поменять на return result для уточнения
            else:
                return ""
                external_api_logger.warning(f"Ошибка request-запроса, status_code: {response.status_code}")

        except  requests.exceptions.RequestException as e:
            external_api_logger.warning(f"Ошибка {e}")
            return ""
    else:
        external_api_logger.warning("Нет даты для получения курса валюты")
        return ""

# для тестовых прогонов:
def get_stock_price_1(stock_name: str) -> float:
    try:
        payload = {"apikey": f"{api_}"}
        response = requests.get(f"{url_}", params=payload)
        result = response.json()
        for elem in result:
            if elem["symbol"] == stock_name:
                price =  round(elem["price"], 2)
            else:
                continue
        if price:
            external_api_logger.info("Получен прайс по акциям")
            return price
        else:
            return float(0)
    except Exception as e:
        external_api_logger.warning(f"Ошибка{e}")
        return float(0)


if __name__ == "__main__":
    user_stocks =  ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

#     my_date = "2023-01-19 05:44:00"
#     #   ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     user_stocks = ["AAPL", "AMZN"]
#
#     price = get_stock_price("2021-01-19 05:44:00", "AAPL")
#     print(price, type(price))
#
#     # timeless_date = get_date(my_date)
#     # rate = get_currency_rate(timeless_date, "USD")
#     # print(rate, type(rate)
    a = get_stock_price_1("AMZN")
    print(a)
    user_stocks =  ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]








