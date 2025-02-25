import json
import logging
import os
from typing import Any

from typing_extensions import Optional

from config import LOGS_DIR

logs_dir = LOGS_DIR
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir, 'services.log'), filemode='w', encoding='utf-8',
                    format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.DEBUG)


def profitability_analysis_of_categories_with_increased_cashback(df_list_dict: list[dict],
                                                                 year: Optional[str | int],
                                                                 month: Optional[str | int]) -> Any:
    """
    JSON с анализом, сколько на каждой категории можно заработать кэшбэка в указанном месяце года.
    """
    logging.info("Запуск анализа...")
    category_cashback: dict = {}
    for value in df_list_dict:
        transaction_date_str = value["Дата операции"]
        day, month_str, rest = transaction_date_str.split('.')
        year_str, _ = rest.split(' ', 1)
        if int(year_str) == year and int(month_str) == month and value["Статус"] == "OK":
            category = value["Категория"]
            if value["Кэшбэк"] is not None and not isinstance(value["Кэшбэк"], float):
                cashback_amount: float | None = float(value["Кэшбэк"])
            else:
                cashback_amount = value["Кэшбэк"]
            if category in category_cashback:
                category_cashback[category] += cashback_amount if cashback_amount is not None else 0
            else:
                category_cashback[category] = cashback_amount if cashback_amount is not None else 0
    filtered_category_cashback = {
        category: round(cashback) if cashback is not None else 0
        for category, cashback in category_cashback.items()
        if cashback > 0
    }
    json_category_dict = json.dumps(filtered_category_cashback, indent=4, ensure_ascii=False)

    logging.info("Результат анализа: %s", json_category_dict)
    logging.info("Анализ завершен")
    return json_category_dict
