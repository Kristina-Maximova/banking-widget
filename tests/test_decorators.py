
from unittest.mock import MagicMock
import json
import pytest
from src.decorators import write_result


@pytest.mark.test
def test_write_result():
    mock_json = MagicMock()
    json.dump = mock_json
    @write_result
    def new_func():
        return 'to json'
    result = new_func()
    assert result == 'to json'
    mock_json.assert_called_once()

