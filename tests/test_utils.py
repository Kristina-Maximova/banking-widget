from unittest.mock import patch
import pandas as pd
import pytest
from src.utils import (read_excel_file, get_list_of_cards,
                       get_data_for_card, get_total_spent,
                       get_top_transactions, get_greeting_by_time,
                       filter_by_date)


@patch("src.utils.pd.read_excel")
def test_read_excel_file(mock_read):
    mock_read.return_value = [{"test": "test1"}]
    a = read_excel_file("fake_path")
    mock_read.assert_called_once()


@patch("src.utils.pd.read_excel")
def test_read_excel_file_empty(mock_read):
    mock_read.return_value = None
    a = read_excel_file("fake_path")
    assert a == {}
    mock_read.assert_called_once()


@pytest.mark.parametrize("time_string, expected", [
    ("2021-11-01 01:00:00", "Доброй ночи"),
    ("2021-11-01 08:00:00", "Доброе утро"),
    ("01.11.2021", "")])
def test_get_greeting_by_time(time_string, expected):
    assert get_greeting_by_time(time_string) == expected



def test_get_list_of_cards(my_test_data):
    cards = get_list_of_cards(my_test_data)
    assert set(cards).issubset(("*4556", "*7197", "*5091"))


def test_filter_by_date(my_test_data):
    result = filter_by_date(my_test_data, '2021-12-30 17:50:30', '2021-12-31 17:50:30', to_datetime=False)
    assert (result.head(1).to_dict(orient="records") ==
            [{'MCC': 5411.0,
              'Бонусы (включая кэшбэк)': 1,
              'Валюта операции': 'RUB',
              'Валюта платежа': 'RUB',
              'Дата операции': '31.12.2021 16:42:04',
              'Дата платежа': '31.12.2021',
              'Категория': 'Супермаркеты',
              'Кэшбэк': None,
              'Номер карты': '*7197',
              'Округление на инвесткопилку': 0,
              'Описание': 'Колхоз',
              'Статус': 'OK',
              'Сумма операции': -64.0,
              'Сумма операции с округлением': 64.0,
              'Сумма платежа': -64.0}])


def test_get_data_for_card(my_test_data):
    assert get_data_for_card(my_test_data, "fake") == []


def test_get_total_spent(my_test_data):
    assert get_total_spent(my_test_data.to_dict(orient="records")) == "21793.45"


def test_get_top_transactions(my_test_data):
    assert (get_top_transactions(my_test_data).head(1).to_dict(orient="records") ==
            [{'Дата операции': '30.12.2021 22:22:03',
              'Дата платежа': '31.12.2021',
              'Категория': 'Переводы',
              'Описание': 'Константин Л.',
              'Сумма операции': -20000.0,
              'Сумма платежа': -20000.0}])


def test_get_list_of_cards_wrong_data():
    """ Обработка неверных данных"""
    this_fake_datas = pd.DataFrame([{"fake": 1}, {"fake1": 11}])
    result = get_list_of_cards(this_fake_datas)
    dataless_data =  pd.DataFrame([])
    result1 =  get_list_of_cards(dataless_data)
    assert result == []
    assert result1 == []



def test_filter_by_date_no_date(my_test_data):
    """ Ошибка, если не задан ходя бы один временной параметр"""
    result = filter_by_date(my_test_data)
    pass






