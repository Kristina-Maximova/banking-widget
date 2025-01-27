import pytest
from src.reports import spending_by_category
from tests.conftest import my_test_data
import datetime


@pytest.mark.test
def test_spending_by_category(my_test_data):
    """ Тест на корректную работу """
    result =  spending_by_category(my_test_data, 'Различные товары', "31.12.2021")
    assert result == '{\n    "Различные товары": 0.0\n}'