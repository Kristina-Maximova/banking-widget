import datetime

date = "2021-05-25 12:05:50"

date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

y_m = date_obj.year, date_obj.month  # кортеж чисел  (2021, 5)

if start_date.strftime("%Y-%m-%d %H:%M") == stop_date.strftime("%Y-%m-%d %H:%M"):
    print("да")
else:
    print("нет")

