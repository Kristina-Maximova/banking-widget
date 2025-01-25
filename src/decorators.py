import json
from functools import wraps
from typing import Callable
from freezegun import freeze_time


from my_logging import decorators_logger
from config import path_to_file_


def write_result(func: Callable) -> Callable:
    """ Записывает результат функции в файл"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = {f"{func.__name__}": func(*args, **kwargs)}
        with open(path_to_file_, "w", encoding="utf-8") as f:
            try:
                json.dump(result, f, ensure_ascii=False, indent=4)
            except json.JSONDecodeError:
                decorators_logger.error(f"Результат {func.__name__} не записан в файл")
        return func(*args, **kwargs)

    return wrapper


def freeze_time(funct, ):
    """Останавливает время при выполнении функции"""


    with freeze_time("2021-07-25 22:10:25"):
        pass
