import os

import re
import pandas as pd
import numpy as np
import datetime
from src.utils import get_card_number

path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "operations.xlsx")



def read_excel_file(path: str) -> pd.DataFrame | dict:
    """Функция для считывания данных из excel-файла, возвращает DataFrame """
    try:
        excel_data = pd.read_excel(path)
        if not excel_data.empty:
            # return list(excel_data.to_dict(orient="records"))
            return excel_data
        else:
            return {}
    except Exception as e:
        print(f"Ошибка при чтении ecxell-файла: {e}")
        return {}


def get_list_of_cards(df_data: pd.DataFrame) -> list:
    "Из данных выводит список уникальных номеров карт"
    # ['*5441', nan, '*5507', '*7197', '*1112', '*5091', '*4556', '*6002']
    # df_data = pd.read_excel(path_to_file)
    if not df_data.empty:
        try:
            notnull_df_data = df_data.dropna(subset=["Номер карты"])
            cards = list(set(notnull_df_data.loc[:,"Номер карты"]))
            return cards
        except Exception:
            return []
    return []


def get_data_by_date(df_data_: pd.DataFrame, date: str) -> pd.DataFrame | dict:
    """Получение выборки из датафрейма по дате"""
    # Убираем пустые строки из выборки:
    df_data1 = df_data_.dropna(how="all")
    # Убираем строки без дат:
    df_data = df_data1.loc[df_data1["Дата операции"].notnull()]
    if date:
        try:
            date_obj = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
            date_str_stop = (f"{date_obj.day}.{date_obj.month}.{date_obj.year}")
            date_obj_stop = datetime.datetime.strptime(date_str_stop, "%d.%m.%Y")
            date_obj_start = date_obj_stop.replace(day=1)
            df_data.loc[:, "Дата операции"] = pd.to_datetime(df_data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
            filtered_df_data = df_data[(df_data["Дата операции"] <= date_obj_stop) & (df_data["Дата операции"] >= date_obj_start)]
            return filtered_df_data
        except Exception as e:
            return {}
    else:
        return {}


# получение выборки для каждой карты
def get_data_for_card(df_data: pd.DataFrame, card: str) -> list:
    """Получение выборки из датафрейма по номеру карты"""
    if not df_data.empty:
        # Установить номер карты в качестве индекса
        # df_data.set_index("Номер карты", inplace=True)
        try:
            sort_data = df_data.loc[df_data["Номер карты"] == card]
            data = list(sort_data.to_dict(orient="records"))
            return data
        except Exception as e:
            return []


def get_total_spent(transactions: list) -> str:
    """Получение суммы трат из списка словарей с операциями, возвращает строку"""
    if transactions:
        amounts = []
        for transaction in transactions:
            if "Сумма операции" in transaction:
                try:
                    amount = float(transaction["Сумма операции"])
                    if amount < 0:
                        amounts.append(amount)
                    else:
                        continue
                except Exception as e:
                    return "00.00"
        if amounts:
            return "{:.2f}".format(abs(sum(amounts)))
        else:
            return "00.00"
    return "00.00"



def get_top_transactions(df_data: pd.DataFrame) -> pd.DataFrame | dict:
    """Функция для получения из датафрейма топ5 транзакций по сумме платежа"""
    if not df_data.empty:
        try:
            selected_columns =  df_data.loc[:,["Сумма операции", "Сумма платежа", "Дата операции", "Категория", "Описание"]]
            top_transactions = selected_columns.sort_values(by=['Сумма платежа']).head(5)
            return top_transactions
        except Exception as e:
            return {}









if __name__ == "__main__":
    dfdata = read_excel_file(path_to_file)
    # Выборка по дате
    df_by_date = get_data_by_date(dfdata, "2021-07-31 5:44:00")
    print(df_by_date[0:3])

    trans_top = get_top_transactions(df_by_date)
    print(trans_top)




    # Список карт
    cards = get_list_of_cards(dfdata)

    print(cards)
    # получаем список словарей c операциями для конкретной карты
    transactions = get_data_for_card(df_by_date, '*4556')
    print(transactions[0:3])

    spent = get_total_spent(transactions)
    cachback = "{:.2f}".format(round((float(spent) * 0.01), 2))
    print(spent)
    print(cachback)









