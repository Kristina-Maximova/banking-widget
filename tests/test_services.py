import pytest

from src.services import investment_bank
from tests.conftest import transacts

# @pytest.mark.parametrize("month_, list_transactions, limit, expected",
#                          [("2021-12", transacts, 50, 207.87),
#                           ("2021-12", transacts, 100, 98.68),
#                           ("2021-12", transacts, 20, 0.0),
#                           ("12.2021", transacts, 50, 0.0)])
# def test_investment_bank(month_, list_transactions, limit, expected):
#     assert investment_bank(month_, list_transactions, limit=limit) == expected


def test_investment_bank_1(transacts):
    assert investment_bank("2021-12", transacts, 50) == 207.87


def test_investment_bank_2(transacts):
    assert investment_bank("2021-07", transacts, 100) == 98.68


def test_investment_bank_3(transacts):
    assert investment_bank("12.2021", transacts, 100) == 0.0
