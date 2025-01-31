import datetime
import json
import re

import pandas as pd

from config import path_to_file, path_to_user_settings
from src.external_api import get_currency_rate, get_stock_price_1  # добавить get_stock_price
from src.my_logging import views_logger
from src.services import investment_bank
from src.settings import get_card_numbers, get_currencies, get_stocks
from src.utils import filter_by_date, get_data_for_card, get_greeting_by_time, get_top_transactions, get_total_spent

my_cards = get_card_numbers(path_to_user_settings)  # ['*7197', '*4556']
my_currencies = get_currencies(path_to_user_settings)  # ['USD', 'EUR']
my_stocks = get_stocks(path_to_user_settings)  # ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']


def create_main_review(dfdata: pd.DataFrame, date: str) -> str:
    """ Принимает данные с транзакциями и
    строку с датой в формате YYYY-MM-DD HH:MM:SS,
    и возвращает JSON-ответ с данными
    """
    try:
        # преобразуем строку с датой в daytime-объект
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        act_start_date = date_obj.replace(day=1)
        start_date_line = act_start_date.strftime("%Y-%m-%d %H:%M:%S")
        # фильтруем по дате с начала месяца до заданной даты
        df_by_date = filter_by_date(dfdata, start_date_=start_date_line, stop_date_=date, to_datetime=False)

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
        views_logger.info("Закончили собирать данные по картам")

        response["top_transactions"] = []
        top_transacts = get_top_transactions(df_by_date)  # тут df
        for index, row in top_transacts.iterrows():
            top = {"date": top_transacts.loc[index, "Дата платежа"]}
            if not pd.isna(top_transacts.loc[index, "Сумма платежа"]):
                top["amount"] = abs(float(top_transacts.loc[index, "Сумма платежа"]))
            else:
                top["amount"] = float(0)
            top["category"] = top_transacts.loc[index, "Категория"]
            top["description"] = top_transacts.loc[index, "Описание"]
            response["top_transactions"].append(top)
        views_logger.info("Закончили собирать данные топ транзакций")

        response["currency_rates"] = []
        if my_currencies:
            timeless_date = date_obj.strftime("%Y-%m-%d")  # '2021-12-16'
            for item in my_currencies:
                currency_data = {"currency": item}
                try:
                    currency_data["rate"] = get_currency_rate(timeless_date, item)  # отдает float
                except Exception:
                    views_logger.warning("не получены курсы валют")
                response["currency_rates"].append(currency_data)
        else:
            views_logger.warning("Нет данных по валютам")
        views_logger.info("Закончили собирать данные курсов валют")

        response["stock_prices"] = []
        if my_stocks:
            for elem in my_stocks:
                stock_data = {"stock": elem}
                try:
                    # get_stock_price_1 можно заменить на get_stock_price,
                    # импортировать из того же модуля
                    # ! eсли get_stock_price(elem, date), то там есть второй аргумент,
                    #  надо вставить   date
                    stock_price = get_stock_price_1(elem)
                    stock_data["price"] = round(float(stock_price), 2)
                except Exception as e:
                    views_logger.warning(f"не получены цены акций, ошибка {e}")
                    stock_data["price"] = float(0)
                response["stock_prices"].append(stock_data)
        else:
            views_logger.warning("нет данных по акциям")
        views_logger.info("Закончили собирать данные по акциям")

        views_logger.info("сформирован json - ответ")

        return json.dumps(response, ensure_ascii=False, indent=4)

    except Exception as e:
        views_logger.error(f"ошибка даты для отчета, ошибка {e}")
        return ""


def create_investment_review(data: pd.DataFrame, date: str, limit: int = 50) -> str:
    """ Принимает pd.DataFrame с транзакциями,
    строку с датой в формате YYYY-MM-DD HH:MM:SS,
    лимит - целое число, шаг округления платежей (по умолчанию 50)
    возвращает json ответ по инвест-накоплениям """
    try:
        transactions = list(data.to_dict(orient="records"))
        date_obg = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        my_month = date_obg.strftime("%Y-%m")
        to_response = investment_bank(my_month, transactions, limit)
        views_logger.info("Сформирован отчет по инвест-накоплениям")
        return json.dumps({"investment": round(to_response, 2)}, ensure_ascii=False, indent=4)
    except Exception as e:
        views_logger.warning(f"Данные по инвест-накоплениям не получены, {e}")
        return json.dumps({"investment": None}, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     my_df_data = read_excel_file(path_to_file)
#     # result = create_main_review(my_df_data, test_date)
#     test_date = "2021-07-31 5:44:00"
#     result_1 = create_investment_review(my_df_data, test_date, 50)

# print(result_1)
