from src.settings import get_card_numbers, get_currencies, get_stocks
from config import path_to_user_settings


def test_get_card_numbers():
    result = get_card_numbers(path_to_user_settings)
    assert result == ["*7197", "*4556"]


def test_get_currencies():
    result = get_currencies(path_to_user_settings)
    assert result == ["USD", "EUR"]


def test_get_stocks():
    result = get_stocks(path_to_user_settings)
    assert result == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
