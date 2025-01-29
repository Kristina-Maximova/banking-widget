import json
from functools import wraps
from typing import Callable

from freezegun import freeze_time

from config import path_to_file_
from src.my_logging import decorators_logger


def write_result(func: Callable) -> Callable:
    """ Записывает результат выполнения функции в файл"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # Вызываем функцию один раз
        result_dict = {f"{func.__name__}": result}
        with open(path_to_file_, "w", encoding="utf-8") as f:
            try:
                json.dump(result_dict, f, ensure_ascii=False, indent=4)
            except json.JSONDecodeError:
                decorators_logger.error(f"Результат {func.__name__} не записан в файл")
        return result  # Возвращаем результат функции

    return wrapper


# def write_result(func: Callable) -> Callable:
#     """ Записывает результат выполнения функции в файл"""
#
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         result = {f"{func.__name__}": func(*args, **kwargs)}
#         with open(path_to_file_, "w", encoding="utf-8") as f:
#             try:
#                 json.dump(result, f, ensure_ascii=False, indent=4)
#             except json.JSONDecodeError:
#                 decorators_logger.error(f"Результат {func.__name__} не записан в файл")
#         return func(*args, **kwargs)
#
#     return wrapper


def write_result_to_my_file(path_to_my_file: str) -> Callable:
    """ Записывает результат выполнения функции в заданный файл """

    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = {f"{func.__name__}": func(*args, **kwargs)}
            with open(path_to_my_file, "w", encoding="utf-8") as f:
                try:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    decorators_logger.error(f"Результат {func.__name__} не записан в файл, ошибка: {e}")
                return func(*args, **kwargs)

        return wrapper

    return my_decorator


def stop_time(date_line: str) -> Callable:
    """
    Останавливает время при выполнении функции
    :argument - cтрока с датой в любом формате (12.01.2014 или 2012-01-31 12:12:12)
    """

    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with freeze_time(date_line):
                return func(*args, **kwargs)

        return wrapper

    return my_decorator

# if __name__ == "__main__":
# @write_result_to_my_file("../results.json")
# @stop_time("21.09.2014")
# def old_time():
#     time = datetime.datetime.now()
#     return time.strftime("%Y-%m-%d")
# a = old_time()
# print(a)
