import logging
import os.path
from datetime import datetime
from typing import Any, Optional

import pandas as pd

from config import LOGS_DIR
from src.utils import transactions_xlsx

logs_dir = LOGS_DIR
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir, 'reports.log'), filemode='w', encoding='utf-8',
                    format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.DEBUG)


def decorator_file(filename: Any) -> Any:

    def my_decorator(function: Any) -> Any:

        def wrapper(transactions: Any, category: Any, date: Any, *args: Any, **kwargs: Any) -> Any:
            logging.info(f"Обработка транзакции для категории: {category} и даты: {date}")
            if isinstance(date, str):
                try:
                    date = pd.to_datetime(date, dayfirst=False)
                except ValueError:
                    date = pd.to_datetime(date, dayfirst=True)

            function(transactions, category, date, *args, **kwargs)

            date_range_start = date - pd.DateOffset(months=3)

            transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

            filtered_transactions = transactions[(transactions['Статус'] == 'OK')
                                                 & (transactions['Дата операции'] >= date_range_start)
                                                 & (transactions['Дата операции'] <= date)
                                                 & (transactions['Категория'] == category)]

            total_amount = round(filtered_transactions['Сумма платежа'].sum(), 2)
            logging.info(f"Запись общей суммы в файл: {filename}")
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"Категория: {category}, Сумма платежа: {total_amount}\n")
            logging.info(f"Завершена обработка транзакции для категории: {category} и даты: {date}")
            return pd.Series([total_amount], name='Сумма платежа')

        return wrapper

    return my_decorator


@decorator_file(filename='expenses_by_category.txt')
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[Any]) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date, dayfirst=True)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)
    filtered_transactions = transactions[(transactions['Статус'] == 'OK')
                                         & (transactions['Дата операции'] <= date)]
    return filtered_transactions[filtered_transactions['Категория'] == category]


transactions = transactions_xlsx
date = datetime.now()
