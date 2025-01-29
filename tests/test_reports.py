from src.reports import spending_by_category


def test_spending_by_category(my_test_data):
    """ Тест на корректную работу """
    result = spending_by_category(my_test_data, 'Различные товары', "28.12.2021")
    assert result == '{\n    "Различные товары": 0.0\n}'
