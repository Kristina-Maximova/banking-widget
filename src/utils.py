import datetime

import pandas as pd

from config import path_to_file
from src.my_logging import utils_logger


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


def filter_by_date(df_data_: pd.DataFrame, start_date_: str = None, stop_date_: str = None,
                   to_datetime: bool = False) -> pd.DataFrame | str:
    """ Фильтрация транзакций по интервалу дат
    :param df_data_ - датафрейм с данными по транзакциям
    :param start_date_ - строка формата ГГГГ-ММ-ДД НН:ММ:SS,
             начало интервала, если не указан - берется текущая дата
    :param stop_date_ - трока формата ГГГГ-ММ-ДД НН:ММ:SS,
            конец интервала, если не указан - берется текущая дата
    :param to_datetime по умолчанию =False. Опционально приведение к типу datetime столбца "Дата операции"
    :return датафрейм с транзакциям в указанном интервале дат
  """
    try:
        # Если не переданы значения одной из дат, генерируем текущую дату
        if start_date_ is None:
            start_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.strptime(start_date_, "%Y-%m-%d %H:%M:%S")
        if stop_date_ is None:
            stop_date = datetime.datetime.now()
        else:
            stop_date = datetime.datetime.strptime(stop_date_, "%Y-%m-%d %H:%M:%S")
        if start_date.strftime("%Y-%m-%d %H:%M") == stop_date.strftime("%Y-%m-%d %H:%M"):

            raise ValueError("Не задан диапазон времени")

        else:
            # пeрeводим столбeц с датой в объект datetime
            df_data_["Дата операции"] = pd.to_datetime(df_data_["Дата операции"], dayfirst=True,
                                                       format="%d.%m.%Y %H:%M:%S")
            # Фильтруем по датам
            filtered_data = df_data_[
                (df_data_["Дата операции"] >= start_date) & (df_data_["Дата операции"] <= stop_date)]
            if to_datetime:
                return filtered_data
            else:
                # возвращаем поле "Дата операции" в исходный str тип
                utils_logger.info("возвращаем столбец 'Дата операции' к исходному типу строки")
                # filtered_data["Дата операции"] =
                # filtered_data["Дата операции"]. apply(lambda x: x.strftime("%d.%m.%Y %H:%M:%S"))
                filtered_data["Дата операции"] = filtered_data["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")
                return filtered_data
    except Exception as e:
        print(f"Не выполнена фильтрация по дате, ошибка: {e}")


def get_data_for_card(df_data: pd.DataFrame, card: str) -> list:
    """Получение выборки из датафрейма по номеру карты, возвращает список словарей"""
    if not df_data.empty:
        try:
            sort_data = df_data.loc[df_data["Номер карты"] == card]
            data = list(sort_data.to_dict(orient="records"))
            return data
        except Exception as e:
            utils_logger.warning(f"Ошибка {e}")
            return []
    return []


def get_total_spent(transactions: list) -> str:
    """Получение суммы трат из списка словарей с операциями, возвращает строку"""
    if transactions:
        amounts = []
        for transaction in transactions:
            if "Сумма платежа" in transaction:
                try:
                    amount = float(transaction["Сумма платежа"])
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
    """ Функция для получения из датафрейма топ-5 транзакций по сумме платежа """
    if not df_data.empty:
        try:
            selected_columns = df_data.loc[:, ["Сумма операции",
                                               "Сумма платежа",
                                               "Дата операции",
                                               "Дата платежа",
                                               "Категория",
                                               "Описание"]]
            top_transactions = selected_columns.sort_values(by=['Сумма платежа']).head(5)
            utils_logger.info("топ_5 по сумме платежа получены")
            return top_transactions
        except Exception as e:
            utils_logger.warning(f"Ошибка {e}")
            return {}


def get_greeting_by_time(time_string: str) -> str:
    """Функция принимает строку с датой формата YYYY-MM-DD HH:MM:SS
    и возвращает приветствие соответственно часам """
    try:
        date_obj = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour
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
        utils_logger.warning("неверный формат даты для get_greeting_by_time")
        return ""


if __name__ == "__main__":
    df_data_1 = read_excel_file(path_to_file)
    df_data_2 = filter_by_date(df_data_1, start_date_="2021-12-01 01:00:00", stop_date_="2021-12-08 01:00:00",
                               to_datetime=False)
    df_data_3 = list(df_data_2.to_dict(orient="records"))

    #     df_data_["Дата операции"] = pd.to_datetime(df_data_["Дата операции"], dayfirst=True,
    #                                                format="%d.%m.%Y %H:%M:%S")
    #     df_data_["Дата операции"] = df_data_["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")

    print(df_data_2.head(4))
