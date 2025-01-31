from unittest.mock import patch

from src.external_api import get_currency_rate, get_stock_price, get_stock_price_1


@patch("requests.get")
def test_get_currency_rate(mock_get):
    """ Тест на корректную работу """
    mock_get.return_value.json.return_value = {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 1},
                                               'info': {'timestamp': 1674172799, 'rate': 69.394157},
                                               'date': '2023-01-19', 'historical': True, 'result': 69.394157}
    mock_get.return_value.status_code = 200
    assert get_currency_rate("2023-01-19", "USD") == 69.39
    mock_get.assert_called_once()


@patch("requests.get")
def test_get_stock_price(mock_get):
    """ Тест на корректную работу """
    a = {'Technical Analysis: MIDPRICE': {'2025-01-20': {'MIDPRICE': '239.7400'},
                                          '2021-01-19': {'MIDPRICE': '126.6064'}}}
    mock_get.return_value.json.return_value = a
    mock_get.return_value.status_code = 200
    assert get_stock_price("2021-01-19 05:44:00", "AAPL") == '126.6064'
    mock_get.assert_called_once()


def test_get_stock_price_no_date():
    """ Тест обработка пустой даты """
    assert get_stock_price("", "AAPL") == ""


@patch("requests.get")
def test_get_stock_price_1(mock_get):
    """ Обработка корректной работы"""
    response = ({'symbol': 'AMSN', 'name': 'Handelsinvest Verden', 'price': 319.4, 'exchange': 'Copenhagen',
                 'exchangeShortName': 'CPH', 'type': 'stock'},
                {'symbol': 'GRPBF', 'name': 'Grupo Lala, S.A.B. de C.V.',
                 'price': 0.84, 'exchange': 'Other OTC',
                 'exchangeShortName': 'PNK', 'type': 'stock'},
                {'symbol': 'HAL.SW', 'name': 'Halliburton Company', 'price': 22.39, 'exchange': 'Swiss Exchange',
                 'exchangeShortName': 'SIX', 'type': 'stock'})
    mock_get.return_value.json.return_value = response
    mock_get.return_value.status_code = 200
    assert get_stock_price_1("AMSN") == 319.4
    mock_get.assert_called_once()
