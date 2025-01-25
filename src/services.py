import os
from typing import Any
import pandas as pd

from src.utils import read_excel_file
from src.manage_dates import check_by_month
path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "operations.xlsx")


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int = 50) -> float:
    """ Принимает аргументы:
    -month - строка в формате 'YYYY-MM',
    -список словарей, содержащий информацию о транзакциях, с полями "Дата операции" и "Сумма операции"
    -limit - предел, до которого нужно округлять суммы операций
    Возвращает сумму, которую можно было бы накопить при округлении трат за указанный месяц
    """
    df_datas = pd.DataFrame(transactions)
    # Фильтруем по месяцу года
    filtered_df = df_datas[df_datas['Дата операции'].apply(lambda x: check_by_month(x, "2021-11"))]
    # Получаем список суммы платежей за этот месяц
    payments = list(filtered_df.loc[:, "Сумма операции"])
    result = 0.0
    for elem in payments:
        if isinstance(elem, float) and elem < 0:
            num = abs(elem)
            # прибавляем разницу между округленным платежом и реальным
            result += (num - (num % limit) + (limit if num % limit != 0 else 0)) - num
    return round(result, 2)


    # Группируем по дате и сумме операции.
    # df_data_ = df_datas.groupby(["Дата операции", "Сумма операции"], as_index=False, dropna=True)
    # Оставляем только выбранные колонки.
    # new_df_data = df_data_[["Дата операции", "Сумма операции"]]
    # Фильтруем по месяцу года
    return payments




if __name__ == "__main__":
    month = "2021-07"
    df_data = read_excel_file(path_to_file)
    transactions = list(df_data.to_dict(orient="records"))
    # print(transactions[0:3])
    a = investment_bank(month, transactions, 50)
    print(a)


    # def round_to_next(elem, limit):
    #     num = abs(elem)
    #     result = (num - (num % limit) + (limit if num % limit != 0 else 0)) - num
    #     return result
    # a = round_to_next(-0.3, 10)
    # print(a)

    investment_bank

