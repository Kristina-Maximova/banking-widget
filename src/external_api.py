import os

import requests
import requests.exceptions
from dotenv import load_dotenv

API_key_currency = os.getenv("API_key_currency")
API_key_shares = os.getenv("API_key_shares")

url = "https://api.apilayer.com/currency_data/historical"

def get_currency_rate(date:str):
    """Функция, возвращающая курс доллара и евро на указанную дату"""
    try:
        payload = {
            "date":

        }
        headers = {
            "apikey": f"{API_key_currency}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        status_code = response.status_code
        result = response.text