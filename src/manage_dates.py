import datetime


def check_by_month(date: str, month: str) -> bool:
    """ Проверяет, что строка формата ДД.MM.ГГГГ HH:MM:SS
    соответствует месяцу в формате ГГГГ-ММ """
    date_obg = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    month_from_date = date_obg.strftime("%Y-%m")
    if month_from_date == month:
        return True
    else:
        return False



if __name__ == "__main__":
    a = check_by_month("03.11.2013 14:55:21", "2013-11")
    print(a)