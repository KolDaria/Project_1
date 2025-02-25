import json
import logging
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from config import LOGS_DIR, PATH_JSON_FILE, PATH_XLSX_FILE

logs_dir = LOGS_DIR
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir, 'utils.log'), filemode='w', encoding='utf-8',
                    format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.DEBUG)

load_dotenv()
api_key = os.getenv('API_KEY')
api_key_fmp = os.getenv('API_KEY_FMP')

path_xlsx_file = PATH_XLSX_FILE
path_json_file = PATH_JSON_FILE


def get_reading_financial_transactions_xlsx(path_xlsx_file: Any) -> Any:
    """
    Считывание финансовых операций из XLSX-файлов.
    """
    logging.info("Чтение XLSX файла")
    try:
        excel_data = pd.read_excel(path_xlsx_file)
        logging.info("Файл считался успешно")
        return excel_data
    except FileNotFoundError:
        logging.warning("Файл не найден")
        return None


transactions_xlsx = get_reading_financial_transactions_xlsx(path_xlsx_file)


def get_json_data_on_the_exchange_rate() -> Any:
    """
    Курс валют в реальном времени.
    """
    try:
        logging.info("Чтение JSON файла...")
        with open(path_json_file, 'r') as file:
            user_settings_dict = json.load(file)
    except FileNotFoundError:
        logging.warning("Файл не найден")
        return "Файл не найден"

    if "user_currencies" not in user_settings_dict:
        logging.error("Ключ 'user_currencies' не найден в JSON файле")
        return "Ключ 'user_currencies' не найден в JSON файле"

    logging.info("Отправка запроса на данные о курсе обмена....")
    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {
        "symbols": ",".join(user_settings_dict["user_currencies"]),
        "base": "RUB"
    }
    headers = {
        "apikey": f"{api_key}"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        status_code = response.status_code
        logging.info(f"Получен ответ с статус кодом: {status_code}")
        if status_code == 200:
            result = response.json()
            logging.info("Данные о курсе обмена успешно выполнены")
            return result
        else:
            logging.error(f"Не удалось получить данные о курсе обмена. Причина ответа: {response.reason}")
            return "Запрос не был успешным."
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")
        return "Произошла ошибка."


def get_jsonparsed_data() -> Any:
    """
    Стоимость акций в реальном времени
    """
    try:
        logging.info("Чтение JSON файла...")
        with open(path_json_file, 'r') as file:
            user_settings_dict = json.load(file)
    except FileNotFoundError:
        logging.warning("Файл не найден")
        return "Файл не найден"

    if "user_stocks" not in user_settings_dict:
        logging.error("Ключ 'user_stocks' не найден в JSON файле")
        return "Ключ 'user_stocks' не найден в JSON файле"

    logging.info("Отправка запроса на данные по акциям....")
    url = (f"https://financialmodelingprep.com/api/v3/quote-short/"
           f"{",".join(user_settings_dict["user_stocks"])}?apikey={api_key_fmp}")
    try:
        response = requests.get(url)
        status_code = response.status_code
        logging.info(f"Получен ответ с статус кодом: {status_code}")
        if status_code == 200:
            result = response.json()
            logging.info("Данные по акциям успешно выполнены")
            return result
        else:
            logging.error(f"Не удалось получить данные по акциям. Причина ответа: {response.reason}")
            return "Запрос не был успешным."
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")
        return "Произошла ошибка."


def top_5_transactions_by_payment_amount(transactions_xlsx: Any) -> Any:
    """
    Получение ТОП-5 транзакций по сумме платежа
    """
    logging.info("Открытие файла с транзакциями")
    if transactions_xlsx is None:
        logging.error("Файл не найден")
        return "Файл не найден"

    logging.info("Провожу фильтрацию данных")

    filtered_transactions_xlsx = transactions_xlsx[(transactions_xlsx['Статус'] == 'OK')
                                                   & (transactions_xlsx['Сумма платежа'] < 0)]

    sorted_transactions = filtered_transactions_xlsx.sort_values(by='Сумма платежа', ascending=True)
    top_5_transactions = sorted_transactions.head(5)

    result_list = []
    for index, row in top_5_transactions.iterrows():
        transaction = {
            "date": row["Дата операции"],
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"]
        }
        result_list.append(transaction)
        logging.info(f"Обработанная транзакция: {transaction}")
    logging.info(f"Возвращено 5 лучших транзакций: {result_list}")
    return result_list


def get_data_for_each_card(transactions_xlsx: Any) -> list[dict]:
    """
    Вывод по каждой карте общей суммы расходов и кэшбэк
    """
    logging.info("Запуск фильтрации...")
    filtered_transactions_xlsx = transactions_xlsx[transactions_xlsx['Статус'] == 'OK']
    result = filtered_transactions_xlsx.groupby(by='Номер карты')['Сумма платежа'].sum()

    result_list = []

    for index, value in result.items():
        last_digits = index[-4:]
        total_spent = abs(value)
        cashback = round(total_spent / 100, 2)
        transaction = {
            "last_digits": last_digits,
            "total_spent": total_spent,
            "cashback": cashback,
        }

        result_list.append(transaction)
        logging.info(f"Обработанная карта: {transaction}")
    logging.info(f"Возвращенные данные по картам: {result_list[1:]}")
    return result_list[1:]
