import pandas as pd
import pytest


@pytest.fixture
def temporary_testing_file() -> str:
    file = "example.xlsx"
    data = {
        'Name': ['John', 'Anna', 'Peter'],
        'Age': [28, 24, 35],
        'City': ['New York', 'Paris', 'Tokyo']
    }
    df = pd.DataFrame(data)
    df.to_excel(file, index=False)
    return file


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    transactions_data = {
        'Статус': ['OK', 'OK', 'OK'],
        'Дата операции': ['2022-01-01', '2022-02-01', '2022-03-01'],
        'Категория': ['Аптеки', 'Аптеки', 'Транспорт'],
        'Сумма платежа': [100, 200, 50]
    }
    return pd.DataFrame(transactions_data)
