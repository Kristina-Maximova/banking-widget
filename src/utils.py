import os

import re
import pandas as pd
import json
import datetime
from src.my_logging import utils_logger

path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "operations.xlsx")
path_to_user_settings = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_settings.json")


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
        utils_logger.warning(f"Ошибка при чтении ecxell-файла: {e}")
        return {}


def get_list_of_cards(df_data: pd.DataFrame) -> list:
    "Из данных выводит список уникальных номеров карт"
    # ['*5441', nan, '*5507', '*7197', '*1112', '*5091', '*4556', '*6002']
    # df_data = pd.read_excel(path_to_file)
    if not df_data.empty:
        try:
            notnull_df_data = df_data.dropna(subset=["Номер карты"])
            cards = list(set(notnull_df_data.loc[:, "Номер карты"]))
            return cards
        except Exception as e:
            utils_logger.warning(f"Ошибка {e}")
            return []
    return []


def get_data_by_date(df_data_: pd.DataFrame, date: str) -> pd.DataFrame | dict:
    """Получение выборки из датафрейма по дате, принимает строку с датой в формате YYYY-MM-DD HH:MM:SS"""
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
            filtered_df_data = df_data[
                (df_data["Дата операции"] <= date_obj_stop) & (df_data["Дата операции"] >= date_obj_start)]
            return filtered_df_data
        except Exception as e:
            utils_logger.warning(f"Ошибка {e}")
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
            utils_logger.warning(f"Ошибка {e}")
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
                    utils_logger.warning(f"Ошибка {e}")
                    return "00.00"
        if amounts:
            utils_logger.info("Сумма трат получена")
            return "{:.2f}".format(abs(sum(amounts)))
        else:
            return "00.00"
    return "00.00"


def get_top_transactions(df_data: pd.DataFrame) -> pd.DataFrame | dict:
    """Функция для получения из датафрейма топ5 транзакций по сумме платежа"""
    if not df_data.empty:
        try:
            selected_columns = df_data.loc[:,
                               ["Сумма операции", "Сумма платежа", "Дата операции", "Дата платежа", "Категория",
                                "Описание"]]
            top_transactions = selected_columns.sort_values(by=['Сумма платежа']).head(5)
            utils_logger.info("топ_5 транзакций по сумме платежа получены")
            return top_transactions
        except Exception as e:
            utils_logger.warning(f"Ошибка {e}")
            print(f"ошибка {e}")
            return {}


def format_date_string(date_line: "str") -> str:
    """Принимает строку с датой формата DD.MM.YYYY HH:MM:SS
    возвращает строку формата YYYY-MM-DD HH:MM:SS
    """
    if date_line:
        try:
            date_obj = datetime.datetime.strptime(date_line, "%d.%m.%Y %H:%M:%S")
            new_date_string = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            return new_date_string
        except Exception as e:
            utils_logger.warning(f"Ошибка {e}")
            return ""
    return ""


def get_date(date_: str) -> str:
    """ Из строкu формата YYYY-MM-DD HH:MM:SS возвращает строку с датой
    формата YYYY-MM-DD"""
    if date_:
        try:
            date_obj = datetime.datetime.strptime(date_, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime("%Y-%m-%d")
        except Exception:
            return ""
    else:
        return ""


def get_month(date: str) -> str:
    """ Из строкu формата YYYY-MM-DD HH:MM:SS возвращает строку с датой
    формата YYYY-MM """
    if date:
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime("%Y-%m")
        except Exception:
            return ""
    return ""


def get_early_date(date: str) -> str:
    """ Принмает строку с датой формата ГГГГ-ММ-DD,
    возвращает строку с датой этого же формата, на 5 дней ранее"""
    if date:
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            new_date_obj = date_obj + datetime.timedelta(days=-5)
            return new_date_obj.strftime("%Y-%m-%d")
        except Exception:
            return ""
    return ""


def get_greeting_by_time(time_string: str) -> str:
    """Функция принимает строку с датой формата YYYY-MM-DD HH:MM:SS
    и возвращает приветствие соответственно часам"""
    if time_string:
        try:
            date_obj = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            hour = date_obj.hour
            if hour:
                utils_logger.info("Подбираем приветствие...")
                if 5 <= hour < 12:
                    return "Доброе утро"
                elif 12 <= hour < 17:
                    return "Добрый день"
                elif 17 <= hour < 22:
                    return "Добрый вечер"
                elif 22 <= hour < 24 or 0 <= hour < 5:
                    return "Доброй ночи"
                else:
                    return ""
        except ValueError:
            return ""
    return ""


# Эту ф. можно потом удалить, если не задействую
def get_card_number(card: str) -> str:
    """ Из строки с номером карты убирает символ звездочки """
    if card:
        card_number = re.sub(r"\*", "", str(card))
        return card_number
    return ""


def get_card_numbers(path: str) -> list:
    """ Функция для считывания номеров карт из json-файла """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            cards = data["user_cards"]
            return cards
    except Exception as e:
        utils_logger.warning(f"Номера карт не получены, ошибка {e}")
        return []


# Timestamp - так объект datetime пишет в консоли: Timestamp('2021-07-30 15:54:47')


if __name__ == "__main__":
    # d = format_date_string('16.12.2021 16:44:00')
    # print(d)
    # h = get_greeting_by_time("2021-12-16 5:44:00")
    # print(h)
    # c = get_card_number("*6578")
    # print(c)
    # date = get_date("2021-12-16 5:44:00")
    # print(date)
    # # month = get_month("2021-12-16 5:44:00")
    # # print(month)
    # dfdata = read_excel_file(path_to_file)
    # # Выборка по дате
    # df_by_date = get_data_by_date(dfdata, "2021-07-31 5:44:00")
    # print(df_by_date[0:3])
    #
    # trans_top = get_top_transactions(df_by_date)
    # print(trans_top)
    #
    # # Список карт
    # cards = get_list_of_cards(dfdata)
    #
    # print(cards)
    # # получаем список словарей c операциями для конкретной карты
    # transactions = get_data_for_card(df_by_date, '*4556')
    # print(transactions[0:3])
    #
    # spent = get_total_spent(transactions)
    # cachback = "{:.2f}".format(round((float(spent) * 0.01), 2))
    # print(spent)
    # print(cachback)
    ldate = get_early_date("2021-01-19")
    print(ldate)
