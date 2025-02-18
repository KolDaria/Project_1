import json
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import (get_data_for_each_card, get_json_data_on_the_exchange_rate, get_jsonparsed_data,
                       get_reading_financial_transactions_xlsx, top_5_transactions_by_payment_amount)


def test_get_reading_financial_transactions_xlsx(temporary_testing_file: Any) -> Any:
    result = get_reading_financial_transactions_xlsx(temporary_testing_file)
    assert result is not None
    assert isinstance(result, pd.DataFrame)


def test_get_reading_financial_transactions_xlsx_not_found() -> Any:
    result = get_reading_financial_transactions_xlsx("")
    assert result is None


@patch("requests.request")
def test_get_json_data_on_the_exchange_rate(mock_get: Any = None) -> Any:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'success': True, 'timestamp': 1739786344, 'base': 'RUB',
                                               'date': '2025-02-17', 'rates': {'USD': 0.010923, 'EUR': 0.010429}}
    assert get_json_data_on_the_exchange_rate() == {'success': True, 'timestamp': 1739786344,
                                                    'base': 'RUB', 'date': '2025-02-17',
                                                    'rates': {'USD': 0.010923, 'EUR': 0.010429}}


@patch("requests.request")
def test_get_json_data_on_the_exchange_rate_invalid_request(mock_get: Any = None) -> Any:
    mock_get.return_value.json.return_value = {'success': True, 'timestamp': 1739786344, 'base': 'RUB',
                                               'date': '2025-02-17', 'rates': {'USD': 0.010923, 'EUR': 0.010429}}
    assert get_json_data_on_the_exchange_rate() == "Запрос не был успешным."


def test_get_json_data_on_the_exchange_rate_file_not_found() -> Any:
    with patch('builtins.open', side_effect=FileNotFoundError()):
        result = get_json_data_on_the_exchange_rate()
        assert result == "Файл не найден"


def test_get_json_data_on_the_exchange_rate_key_not_found() -> Any:
    user_settings_dict: dict = {}
    with patch('builtins.open', mock_open(read_data=json.dumps(user_settings_dict))):
        result = get_json_data_on_the_exchange_rate()
        assert result == "Ключ 'user_currencies' не найден в JSON файле"


def test_get_json_data_on_the_exchange_rate_exception_handling() -> Any:
    user_settings_dict = {"user_currencies": ["USD", "EUR"]}
    with patch('builtins.open', mock_open(read_data=json.dumps(user_settings_dict))):
        with patch('requests.request') as mock_request:
            mock_request.side_effect = Exception("Test exception")
            result = get_json_data_on_the_exchange_rate()
            assert result == "Произошла ошибка."


def test_get_jsonparsed_data_file_not_found() -> Any:
    with patch('builtins.open', side_effect=FileNotFoundError()):
        result = get_jsonparsed_data()
        assert result == "Файл не найден"


def test_get_jsonparsed_data_key_not_found() -> Any:
    user_settings_dict: dict = {}
    with patch('builtins.open', mock_open(read_data=json.dumps(user_settings_dict))):
        result = get_jsonparsed_data()
        assert result == "Ключ 'user_stocks' не найден в JSON файле"


def test_get_jsonparsed_data_exception_handling() -> Any:
    user_settings_dict = {"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    with patch('builtins.open', mock_open(read_data=json.dumps(user_settings_dict))):
        with patch('requests.get') as mock_request:
            mock_request.side_effect = Exception("Test exception")
            result = get_jsonparsed_data()
            assert result == "Произошла ошибка."


@patch("requests.get")
def test_get_jsonparsed_data_invalid_request(mock_get: Any = None) -> Any:
    mock_get.return_value.json.return_value = [{'symbol': 'AAPL', 'price': 244.6, 'volume': 40896227}]
    assert get_jsonparsed_data() == "Запрос не был успешным."


@patch("requests.get")
def test_get_jsonparsed_data(mock_get: Any = None) -> Any:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'symbol': 'AAPL', 'price': 244.6, 'volume': 40896227}]
    assert get_jsonparsed_data() == [{'symbol': 'AAPL', 'price': 244.6, 'volume': 40896227}]


def test_top_5_transactions_by_payment_amount_not_found() -> Any:
    result = top_5_transactions_by_payment_amount(None)
    assert result == "Файл не найден"


def test_top_5_transactions_by_payment_amount() -> Any:
    data = {
        'Статус': ['OK', 'OK', 'OK', 'OK', 'OK', 'Failed'],
        'Сумма платежа': [-100, -50, -200, -150, -250, -300],
        'Дата операции': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06'],
        'Категория': ['Перевод', 'Покупка', 'Перевод', 'Покупка', 'Перевод', 'Покупка'],
        'Описание': ['Описание1', 'Описание2', 'Описание3', 'Описание4', 'Описание5', 'Описание6']
    }
    transactions_xlsx = pd.DataFrame(data)
    result = top_5_transactions_by_payment_amount(transactions_xlsx)
    assert len(result) <= 5


def test_get_data_for_each_card() -> Any:
    data = {
        'Статус': ['OK', 'OK', 'Not OK', 'OK'],
        'Номер карты': ['1234-5678-9012-3456', '1234-5678-9012-3457', '1234-5678-9012-3458', '1234-5678-9012-3456'],
        'Сумма платежа': [-100.0, -200.0, -50.0, -300.0]
    }
    transactions_xlsx = pd.DataFrame(data)
    result = get_data_for_each_card(transactions_xlsx)
    assert len(result) == 1
    assert result[0]['last_digits'] == '3457'
    assert result[0]['total_spent'] == 200.0
    assert result[0]['cashback'] == 2.0


def test_get_data_for_each_card_empty_input() -> Any:
    transactions_xlsx = pd.DataFrame({
        'Статус': [],
        'Номер карты': [],
        'Сумма платежа': []
    })
    result = get_data_for_each_card(transactions_xlsx)
    assert result == []


def test_get_data_for_each_card_no_ok_status() -> Any:
    transactions_xlsx = pd.DataFrame({
        'Статус': ['Not OK'],
        'Номер карты': ['1234-5678-9012-3456'],
        'Сумма платежа': [-100.0]
    })
    result = get_data_for_each_card(transactions_xlsx)
    assert len(result) == 0
