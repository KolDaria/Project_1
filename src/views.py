import json
import logging
import os
from datetime import datetime
from typing import Any

from config import LOGS_DIR
from src.utils import (get_data_for_each_card, get_json_data_on_the_exchange_rate, get_jsonparsed_data,
                       top_5_transactions_by_payment_amount, transactions_xlsx)

logs_dir = LOGS_DIR
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir, 'views.log'), filemode='w', encoding='utf-8',
                    format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.DEBUG)


def location_of_the_main_function(date: str | None = None) -> Any:
    """
    Возвращает JSON-ответ со всеми реализованными функциями.
    """
    logging.info("Выполнение функции началось")

    if date is None:
        end_period = datetime.now()
    else:
        end_period = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    hour = end_period.hour
    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 24:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    welcome_dict: dict = {
        "greeting": greeting
    }

    cards = get_data_for_each_card(transactions_xlsx)
    top_transactions = top_5_transactions_by_payment_amount(transactions_xlsx)
    currency_rates = get_json_data_on_the_exchange_rate()
    stock_prices = get_jsonparsed_data()

    welcome_dict["cards"] = cards
    welcome_dict["top_transactions"] = top_transactions
    welcome_dict["currency_rates"] = currency_rates
    welcome_dict["stock_prices"] = stock_prices

    json_welcome_dict = json.dumps(welcome_dict, indent=4, ensure_ascii=False)

    logging.info("Функция выполнилась успешно")
    return json_welcome_dict
