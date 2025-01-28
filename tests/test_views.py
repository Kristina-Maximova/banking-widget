import pytest

from unittest.mock import patch
from src.views import create_main_review


@patch("src.external_api.get_stock_price")
@patch("src.external_api.get_currency_rate")
def test_create_main_review(mock_get_1, mock_get_2, my_test_data):
     """ Тест на корректную работу"""
     pass
#     mock_get_2.return_value.json.return_value= [{"symbol": "USD", "price": 10.0},{"symbol": "EUR", "ice": 20.0}]
#     mock_get_1.return_value.json.return_value = [{"result":1.1}, ]
#     result = create_main_review(my_test_data, "2021-12-30 00:00:00")
#     assert result == {"jkj"}
#     mock_get_1.assert_called()
#     mock_get_2.assert_called()

