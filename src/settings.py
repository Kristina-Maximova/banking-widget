import json
from typing import Any

from src.my_logging import settings_logger


def get_card_numbers(path: str) -> list | Any:
    """ Функция для считывания номеров карт из json-файла """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            cards = data["user_cards"]
            return cards
    except Exception as e:
        settings_logger.warning(f"Номера карт не получены, ошибка {e}")
        return []


def get_currencies(path: str) -> list | Any:
    """ Считывание валют из настроек в json-файле"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            cards = data["user_currencies"]
            return cards
    except Exception as e:
        settings_logger.warning(f"Значения валют не получены, ошибка {e}")
        return []


def get_stocks(path: str) -> list | Any:
    """ Считывание валют из настроек в json-файле"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            cards = data["user_stocks"]
            return cards
    except Exception as e:
        settings_logger.warning(f"Значения акций не получены, ошибка {e}")
        return []

# if __name__ == "__main__":
#     my_stocks = get_stocks(path_to_user_settings)
#     print(my_stocks)

# with open(r"..\user_settings.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
