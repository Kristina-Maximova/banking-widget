import json
from datetime import date
from unittest.mock import MagicMock

import pytest

from src.decorators import stop_time, write_result, write_result_to_my_file


def test_write_result():
    mock_json = MagicMock()
    json.dump = mock_json

    @write_result
    def new_func():
        return 'to json'

    result = new_func()
    assert result == 'to json'
    mock_json.assert_called_once()


@write_result_to_my_file("Fake_path")
def example_function():
    a = float("test")
    print(a)
    raise ValueError("Округлить строку не получится")


def test_write_result_to_my_file():
    @write_result_to_my_file("Fake_path")
    def example_function():
        a = float("test")
        print(a)
        raise ValueError("Округлить строку не получится")

    with pytest.raises(ValueError, match="could not convert string to float"):
        example_function()


def test_stop_time():
    @stop_time("2012-01-31 12:12:12")
    def current_time():
        my_current_day = date.today()
        return my_current_day

    my_fake_time = current_time()
    assert my_fake_time != date.today()
