from typing import Any

import pandas as pd
import pytest

from src.reports import spending_by_category


def test_spending_by_category(transactions_df: pd.DataFrame) -> Any:
    result = spending_by_category(transactions_df, 'Аптеки', "2020-12-05")
    assert result.shape[0] > 0


def test_decorator_file(transactions_df: pd.DataFrame) -> Any:
    result = spending_by_category(transactions_df, 'Аптеки', "2020-12-05")
    assert isinstance(result, pd.Series)


def test_file_creation(transactions_df: pd.DataFrame) -> Any:
    spending_by_category(transactions_df, 'Аптеки', "2020-12-05")
    try:
        with open('expenses_by_category.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            assert 'Категория: Аптеки' in content
    finally:
        import os
        os.remove('expenses_by_category.txt')


def test_spending_by_category_with_invalid_date(transactions_df: pd.DataFrame) -> Any:
    date = "invalid-date"
    with pytest.raises(ValueError):
        spending_by_category(transactions_df, 'Аптеки', date)
