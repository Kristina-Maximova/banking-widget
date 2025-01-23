import os

import requests
import requests.exceptions
from dotenv import load_dotenv
from src.utils import get_date, get_month

load_dotenv()
API_key_currency = os.getenv("API_key_currency")
API_key_shares = os.getenv("API_key_shares")

url = "https://api.apilayer.com/exchangerates_data/convert"
# в этом апи-ключ в параметрах идет:
url = "https://www.alphavantage.co/query"


def get_currency_rate(date_: str, currency: str = "USD"):
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
            result = response.json()  # ответ от сервера
            return round(result["result"], 2)

        else:
            print(f"Ошибка: {response.status_code}")
            return float(0)
    except requests.exceptions.RequestException as e:
        return float(0)


def get_stock_price(date_line: str, stock_name: str) -> str:
    """ Функция принимает строку с датой и название акции, и
    возвращает среднюю за месяц стоимость акции"""
    # за 30.12.ГГГГ и 31.12.ГГГГ нет данных на сайте
    date = get_date(date_line)
    month = get_month(date_line)
    if date != "" and month != "":
        try:
            payload = {
                "function": "MIDPRICE",
                "symbol": f"{stock_name}",
                "interval": "daily",
                "month": "2009-01",
                "time_period": "30",
                "apikey": f"{API_key_shares}"
            }
            response = requests.get("https://www.alphavantage.co/query", params=payload)
            status_code = response.status_code
            if status_code == 200:
                try:
                    result = response.json()  # ответ от сервера
                    new_result = result['Technical Analysis: MIDPRICE'][f"{date}"]['MIDPRICE']
                    return new_result
                except Exception:
                    return ""
                    print("ошибка обработки json - ответа")
            else:
                return ""
                print(f"Ошибка request-запроса, status_code: {response.status_code}")

        except  requests.exceptions.RequestException as e:
            print(f"Ошибка {e}")
            return ""


if __name__ == "__main__":
    my_date = "2021-12-16 5:44:00"
    # "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price = get_stock_price(my_date, "TSLA")
    print(price)
