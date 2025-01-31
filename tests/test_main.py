from unittest.mock import patch

from src.main import main


@patch("src.main.spending_by_category", return_value="")
@patch("src.main.create_investment_review", return_value="")
@patch("src.main.create_main_review", return_value="")
def test_main(mock_get_1, mocr_get_2, mock_get_3):
    main()
    mock_get_1.assert_called()
    mocr_get_2.assert_called()
    mock_get_3.assert_called()
