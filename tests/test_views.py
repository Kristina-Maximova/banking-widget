import pytest
import json
from unittest.mock import patch
from src.views import create_main_review


@patch("src.external_api.get_stock_price_1", return_value= 91.1)
def test_create_main_review(mock_get_1, my_test_data):

     result = create_main_review(my_test_data, "2021-12-30 00:00:00")
     assert json.loads(result) == "knk"
     mock_get_1.assert_called()

