import os
import re
import pandas as pd
import json

from src.utils import (read_excel_file,
                       get_greeting_by_time,
                       get_data_by_date,
                       get_total_spent,
                       get_data_for_card,
                       get_top_transactions,
                       get_date)
from src.settings import (get_card_numbers,
                          get_currencies,
                          get_stocks)
from src.my_logging import views_logger

from src.external_api import get_currency_rate, get_stock_price, get_stock_price_1  # No error

path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "operations.xlsx")
path_to_user_settings = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_settings.json")

my_cards = get_card_numbers(path_to_user_settings)  # ['*7197', '*4556']
my_currencies = get_currencies(path_to_user_settings)  # ['USD', 'EUR']
my_stocks = get_stocks(path_to_user_settings)  # ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']


def create_response(date: str) -> dict:
    """ Принимает строку с датой в формате YYYY-MM-DD HH:MM:SS, 
    и возвращает JSON-ответ с данными """
    dfdata = read_excel_file(path_to_file)
    df_by_date = get_data_by_date(dfdata, date)

    actual_greeting = get_greeting_by_time(date)
    response = {"greeting": actual_greeting}

    response["cards"] = []
    if my_cards:
        for elem in my_cards:
            transactions = get_data_for_card(df_by_date, elem)  # тут лист, а не df
            cards_data = {"last_digits": re.sub(r"\*", "", elem)}
            spent = get_total_spent(transactions)
            cards_data["total_spent"] = float(spent)
            cards_data["cashback"] = (round((float(spent) * 0.01), 2))
            response["cards"].append(cards_data)
    else:
        views_logger.warning("Данные по картам отсутствуют")

    response["top_transactions"] = []
    top_transacts = get_top_transactions(df_by_date)  # тут df
    for index, row in top_transacts.iterrows():
        top = {"date": top_transacts.loc[index, "Дата платежа"]}
        if not pd.isna(top_transacts.loc[index, "Сумма платежа"]):
            top["amount"] = float(top_transacts.loc[index, "Сумма платежа"])
        else:
            top["amount"] = float(0)
        top["category"] = top_transacts.loc[index, "Категория"]
        top["description"] = top_transacts.loc[index, "Описание"]
        response["top_transactions"].append(top)

    response["currency_rates"] = []
    if my_currencies:
        timeless_date = get_date(date)  # '2021-12-16'
        for item in my_currencies:
            currency_data = {"currency": item}
            try:
                currency_data["rate"] = get_currency_rate(timeless_date, item)  # отдает float
            except Exception:
                views_logger.warning("не получены курсы валют")
            response["currency_rates"].append(currency_data)
    else:
        views_logger.warning("Нет данных по валютам")

    response["stock_prices"] = []
    if my_stocks:
        for elem in my_stocks:
            stock_data = {"stock": elem}
            try:
                # ! eсли get_stock_price(elem, date), то есть второй аргумент
                stock_price = get_stock_price_1(elem)
                stock_data["price"] = round(float(stock_price), 2)
            except Exception as e:
                views_logger.warning(f"не получены цены акций, ошибка {e}")
                stock_data["price"] = float(0)
            response["stock_prices"].append(stock_data)
    else:
        views_logger.warning("нет данных по акциям")

    views_logger.info("сформирован json - ответ")
    return json.dumps(response, ensure_ascii=False)


if __name__ == "__main__":
    test_date = "2021-07-31 5:44:00"
    result = create_response(test_date)
    print(result)
