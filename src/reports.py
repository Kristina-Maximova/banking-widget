import datetime
import json

import pandas as pd

from config import path_to_file
from src.my_logging import reports_logger
from src.utils import filter_by_date, read_excel_file


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: str = None) -> str:
    """
    Фильтрация транзакций по заданной категории трат за 3 мес.
    :param transactions: датафрейм с данными о транзакциях
    :param category: строка с названием категории
    :param date: строка формата DD.MM.YYYY
    :return: json-строка с тратами по заданной категории за последние три месяца
    (от переданной даты).
    """
    # получаем даты для фильтрации
    if date is None:
        stop_date_obj = datetime.datetime.today()
    else:
        stop_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_date_obj = stop_date_obj - datetime.timedelta(days=90)
    start_line = start_date_obj.strftime("%Y-%m-%d %H:%M:%S")
    stop_line = stop_date_obj.strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Получаем данные за последние 3 мес
        filtered_data = filter_by_date(transactions, start_line, stop_line, to_datetime=True)
        # Фильтрация по заданной категории и отрицательным значениям суммы платежа
        data_by_category = filtered_data.loc[
            (filtered_data["Категория"] == category.title()) & (filtered_data["Сумма платежа"] < 0)]
        # Выбираем нужные столбцы и суммируем значения
        selected_data = data_by_category[["Категория", "Сумма платежа"]].groupby("Категория").sum()
        payments = abs(selected_data.to_dict(orient="records")[0]["Сумма платежа"])
        reports_logger.info("траты по категориям получены")
        return json.dumps({category: payments}, ensure_ascii=False, indent=4)
    except Exception as e:
        reports_logger.warning(f"Данные трат по категориям не получены, ошибка {e}")
        return json.dumps({category: 0.0}, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     my_date = "2021-07-31 5:44:00"
#     date_obj = datetime.datetime.strptime(my_date, "%Y-%m-%d %H:%M:%S")
#     date_for_reports = date_obj.strftime("%d.%m.%Y")
#     category = "Супермаркеты"
#
#     transacts_ = read_excel_file(path_to_file)  # датафр
#     my_result = spending_by_category(transacts_, category, "31.07.2021")

# filtered_data = filter_by_date(transacts_, start_line, stop_line, to_datetime=True)
# data_by_category = filtered_data.loc[
#     (filtered_data["Категория"] == category.title()) & (filtered_data["Сумма платежа"] < 0)]
# selected_data  = data_by_category[["Категория", "Сумма платежа"]].groupby("Категория").sum()
# payments = abs(selected_data.to_dict(orient="records")[0]["Сумма платежа"])
# # print(transacts.head(10).to_dict(orient="records"))
# print(my_result)
