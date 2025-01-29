from unittest.mock import patch
from src.views import create_main_review, create_investment_review
from tests.conftest import my_test_data
import pandas as pd


@patch("src.views.get_currency_rate", return_value=91.1)
@patch("src.views.get_stock_price_1", return_value=91.1)
def test_create_main_review(mock_get_1, mock_get_2, my_test_data):
    """ Тест на обработку корректных данных"""
    dfdata_to_test = my_test_data
    date_to_test = "2021-12-30 01:00:00"
    result = create_main_review(dfdata_to_test, date_to_test)
    mock_get_1.assert_called()
    mock_get_2.assert_called()





def test_create_main_review_wrong_data():
    """ Тест на работу при отсутствии данных по картам и валюте"""
    with patch("src.views.get_stocks") as mock_get:
        mock_get.return_value = []

        with patch("src.views.get_currencies") as mock_get_1:
            mock_get_1.return_value = []

            this_fake_transacts = pd.DataFrame([{"fake": 1}, {"fake1": 11}])
            this_fake_date = "2021-07-31 05:44:00"
            result = create_main_review(this_fake_transacts, this_fake_date)
            assert result == ""


def test_create_investment_review(my_test_data):
    """ Тест на корректную работу"""
    result = create_investment_review(my_test_data, "2021-12-31 05:44:00", 100)
    assert result == '{\n    "investment": 307.87\n}'
