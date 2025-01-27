from config import path_to_file
from src.reports import spending_by_category
from src.views import read_excel_file, create_main_review, create_investment_review

import datetime


my_dfdata = read_excel_file(path_to_file)
my_date = "2021-07-31 5:44:00" # строка формата ГГГГ-ММ-ДД
my_limit = 50   # шаг округления сумм для инвест-накоплений
my_category = "Супермаркеты"

def main(date: str) -> list:

    date_obj = datetime.datetime.strptime(my_date, "%d.%m.%Y %H:%M:%S")
    result = []
    to_home_page = create_main_review(my_dfdata, my_date)
    result.append(to_home_page)

    to_services = create_investment_review(my_dfdata, my_date, my_limit)
    result.append(to_services)

    date_for_reports = date_obj.strftime("%d.%m.%Y")
    to_reports = spending_by_category(my_dfdata, my_category, date_for_reports )
    result.append(to_reports)

    return result


if __name__ == "__main__":
    main(my_date)
