import json
from typing import Any

from src.services import profitability_analysis_of_categories_with_increased_cashback


def test_profitability_analysis_of_categories_with_increased_cashback() -> Any:
    df_list_dict = [
        {"Дата операции": "01.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": "10.0"},
        {"Дата операции": "02.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": "20.0"},
        {"Дата операции": "01.02.2022 00:00:00", "Статус": "OK", "Категория": "Путешествие", "Кэшбэк": "30.0"},
    ]
    year = 2022
    month = 1
    result = profitability_analysis_of_categories_with_increased_cashback(df_list_dict, year, month)
    assert json.loads(result) == {"Аптеки": 30}


def test_profitability_analysis_of_categories_with_increased_cashback_zero_cashback() -> Any:
    df_list_dict = [
        {"Дата операции": "01.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": "0.0"},
        {"Дата операции": "02.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": "0.0"},
    ]
    year = 2022
    month = 1
    result = profitability_analysis_of_categories_with_increased_cashback(df_list_dict, year, month)
    assert json.loads(result) == {}


def test_profitability_analysis_of_categories_with_increased_cashback_empty_df_list_dict() -> Any:
    df_list_dict: list = []
    year = 2022
    month = 1
    result = profitability_analysis_of_categories_with_increased_cashback(df_list_dict, year, month)
    assert json.loads(result) == {}


def test_profitability_analysis_of_categories_with_increased_cashback_none_cashback() -> Any:
    df_list_dict = [
        {"Дата операции": "01.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": None},
        {"Дата операции": "02.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": None},
    ]
    year = 2022
    month = 1
    result = profitability_analysis_of_categories_with_increased_cashback(df_list_dict, year, month)
    assert json.loads(result) == {}
