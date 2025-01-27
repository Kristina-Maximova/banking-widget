
from unittest.mock import patch
from src.external_api import get_currency_rate, get_stock_price, get_stock_price_1


@patch("requests.get")
def test_get_currency_rate(mock_get):
    mock_get.return_value.json.return_value = {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 1},
                                               'info': {'timestamp': 1674172799, 'rate': 69.394157},
                                               'date': '2023-01-19', 'historical': True, 'result': 69.394157}
    mock_get.return_value.status_code = 200
    assert get_currency_rate("2023-01-19", "USD") == 69.39
    mock_get.assert_called_once()



@patch("requests.get")
def test_get_stock_price(mock_get):
    mock_get.return_value.json.return_value = ""


