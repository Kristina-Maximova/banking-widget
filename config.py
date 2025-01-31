import os

PATH = os.path.dirname(os.path.abspath(__file__))  # путь до текущего файла
path_to_file = os.path.join(PATH, "data", "operations.xlsx")  # файл с данными о транзакциях
path_to_logfile = os.path.join(PATH, "logs", "my_logs.log")  # для записи логов
path_to_user_settings = os.path.join(PATH, "user_settings.json")
path_to_file_ = os.path.join(PATH, "results.json")  # путь для декоратора записи в файл
