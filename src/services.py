import datetime

import pandas as pd
from src.decorators import write_result
from src.my_logging import services_logger
from config import path_to_file
from src.utils import read_excel_file


def investment_bank(month_: str, list_transactions: list, limit: int = 50) -> float:
    """ Принимает аргументы:
    :arg-month - строка в формате 'YYYY-MM',
    :arg-transactions - список словарей, содержащих ключи "Дата операции" и "Сумма платежа"
    :arg-limit - шаг округления сумм ( по-умолчанию 50
    :return суммa, которую можно было бы накопить при округлении трат за указанный месяц
    """
    try:
        df_datas = pd.DataFrame(list_transactions)
        # Фильтруем по месяцу года
        filtered_df = df_datas[df_datas['Дата операции'].apply(lambda x: check_by_month(x, month_))]
        # Получаем список суммы платежей за этот месяц
        payments = list(filtered_df.loc[:, "Сумма платежа"])
        services_logger.info("investment_bank - cуммы платежей получены")
        result = 0.0
        for elem in payments:
            if isinstance(elem, float) and elem < 0:
                num = abs(elem)
                # прибавляем разницу между округленным платежом и реальным
                result += (num - (num % limit) + (limit if num % limit != 0 else 0)) - num
            else:
                continue
        services_logger.info("Накопления для инвест-банка получены")
        return round(result, 2)
    except Exception as e:
        services_logger.warning(f"Ошибка выполнения функции investment_bank: {e}")
        return float(0)


def check_by_month(date: str, my_month: str) -> bool:
    """ Предикат, проверяющий, что строка формата ДД.MM.ГГГГ HH:MM:SS
    соответствует месяцу в формате ГГГГ-ММ """
    date_obg = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    month_from_date = date_obg.strftime("%Y-%m")
    if month_from_date == my_month:
        return True
    else:
        return False

    # Группируем по дате и сумме операции.
    # df_data_ = df_datas.groupby(["Дата операции", "Сумма операции"], as_index=False, dropna=True)
    # Оставляем только выбранные колонки.
    # new_df_data = df_data_[["Дата операции", "Сумма операции"]]
    # Фильтруем по месяцу года


# if __name__ == "__main__":
#     new_month = "2021-12"
    # df_data = read_excel_file(path_to_file)
    # this_transactions = list(df_data.to_dict(orient="records"))[0:10]  # тут даты так: '31.12.2021 16:44:00'
    # a = investment_bank(new_month, this_transactions, 50)

    # # Округляем до большего значения с заданным шагом
    # def round_to_next(elem, limit):
    #     num = abs(elem)
    #     result = (num - (num % limit) + (limit if num % limit != 0 else 0)) - num
    #     return result
    # a = round_to_next(-0.3, 10)
    # print(a)
