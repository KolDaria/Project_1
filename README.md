# Проект 1. "Приложение для анализа банковских операций"

## **Описание:**

Проект "Приложение для анализа банковских операций" - приложение, которое будет генерировать JSON-данные для веб-страниц, 
формировать Excel-отчеты, а также предоставлять другие сервисы.
 

## **Установка:**

Версия python для данного проекта `^3.13`

1. Установите Poetry:
```
https://install.python-poetry.org | python -
```
2. Клонируйте репозиторий:
```
git clone https://github.com/KolDaria/Project_1
```
3. Установите зависимости:
```
poetry add requests
```

## **Использование:**

### *Проект содержит:*

#### Папку `src` в которой реализованны следующие функции:

1. `__init__`: инициализация объекта.
2. `get_reading_financial_transactions_xlsx`: функция считывает финансовые операций из XLSX-файла.
3. `get_json_data_on_the_exchange_rate`: функция определяет курс валют в реальном времени.
4. `get_jsonparsed_data`: функция определяет стоимость акций в реальном времени.
5. `top_5_transactions_by_payment_amount`: функция возвращает ТОП-5 транзакций по сумме платежа. 
6. `get_data_for_each_card`: функция возвращает вывод по каждой карте общей суммы расходов и кэшбэк.
7. `location_of_the_main_function`: функция возвращает JSON-ответ со всеми реализованными выше функциями.
8. `profitability_analysis_of_categories_with_increased_cashback`: функция возвращает JSON с анализом, сколько на 
каждой категории можно заработать кэшбэка в указанном месяце года.
9. `spending_by_category`: функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
10. `main.py`: функция связывающая функциональности между собой.

#### Папку `tests` в которой реализованно следующее:

1. `__init__`: инициализация объекта.
2. `test_utils.py`: модуль для тестирования функций `get_reading_financial_transactions_xlsx, 
get_json_data_on_the_exchange_rate, get_jsonparsed_data, top_5_transactions_by_payment_amount, get_data_for_each_card`.
3. `test_viewst.py`: модуль для тестирования функций `location_of_the_main_function`.
4. `test_services.py`: модуль для тестирования функций `profitability_analysis_of_categories_with_increased_cashback`.
5. `test_reports.py`: модуль для тестирования функций `spending_by_category`

#### Папку `data` которая содержит:

1. `operations.xlsx`: файл транзакций.
2. `user_settings.json`: файл пользовательских настроек.

##### Примеры использования функций `get_reading_financial_transactions_xlsx, get_json_data_on_the_exchange_rate, get_jsonparsed_data, top_5_transactions_by_payment_amount, get_data_for_each_card`:

```python
# Пример для функции get_reading_financial_transactions_xlsx
import pandas as pd
import os

path_file = os.path.dirname(__file__)  # входной аргумент
result = pd.DataFrame  # выход функции

# Пример для функции get_json_data_on_the_exchange_rate
["USD", "EUR"]  # входной аргумент
{'success': True, 'timestamp': 1739786344, 'base': 'RUB', 'date': '2025-02-17', 'rates': {'USD': 0.010923, 'EUR': 0.010429}}  # выход функции

# Пример для функции get_jsonparsed_data
["AAPL"]  # входной аргумент
[{'symbol': 'AAPL', 'price': 244.6, 'volume': 40896227}]  # выход функции

# Пример для функции top_5_transactions_by_payment_amount
data =  {
        "Статус": ["OK", "OK", "OK", "OK", "OK", "Failed"],
        "Сумма платежа": [-100, -50, -200, -150, -350, -200],
        "Дата операции": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06"],
        "Категория": ["Перевод", "Перевод", "Перевод", "Перевод", "Перевод", "Перевод"],
        "Описание": ["Лента", "Лента", "Лента", "Лента", "Лента", "Лента"]
    } # входной аргумент
{
      "date": "20.01.2022",
      "amount": 850.00,
      "category": "Перевод",
      "description": "Лента"
    }  # выход функции

# Пример для функции get_data_for_each_card
data = {
        "Статус": ["OK", "OK", "Not OK", "OK"],
        "Номер карты": ["1234-5678-9012-3457", "1234-5678-9012-3458", "1234-5678-9012-3456", "1256-4589-4568-2587"],
        "Сумма платежа": [-1262.0, -200.0, -50.0, -300.0]
    } # входной аргумент
{
      "last_digits": "3457",
      "total_spent": 1262.00,
      "cashback": 12.62
    }  # выход функции
```

##### Примеры использования функций `location_of_the_main_function`:

```python
# Пример для функции location_of_the_main_function
"2020-10-12 02:10:47" # входной аргумент
"Доброй ночи" # выход функции
```

##### Примеры использования функций `profitability_analysis_of_categories_with_increased_cashback`:

```python
# Пример для функции profitability_analysis_of_categories_with_increased_cashback
# входной аргумент
df_list_dict = [
        {"Дата операции": "01.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": "10.0"},
        {"Дата операции": "02.01.2022 00:00:00", "Статус": "OK", "Категория": "Аптеки", "Кэшбэк": "20.0"},
        {"Дата операции": "01.02.2022 00:00:00", "Статус": "OK", "Категория": "Путешествие", "Кэшбэк": "30.0"},
    ]
    year = 2022
    month = 1  
{"Аптеки": 30} # выход функции
```

##### Примеры использования функций `spending_by_category`:

```python
# Пример для функции spending_by_category
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[Any]) -> pd.DataFrame:
    pass
Ожидаемый вывод в example.txt

при успешном выполнении:
Категория: "Аптеки", Сумма платежа: 1258.25
```

## Тестирование функций:

```
---------- coverage: platform win32, python 3.13.0-final-0 -----------
Name                     Stmts   Miss  Cover
--------------------------------------------
config.py                    6      0   100%
src\__init__.py              0      0   100%
src\reports.py              41      1    98%
src\services.py             29      0   100%
src\utils.py               110      0   100%
src\views.py                35      0   100%
tests\__init__.py            0      0   100%
tests\conftest.py           13      0   100%
tests\test_reports.py       22      0   100%
tests\test_services.py      27      0   100%
tests\test_utils.py         86      0   100%
tests\test_views.py         22      0   100%
--------------------------------------------
TOTAL                      391      1    99%
```

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](docs/README.md).

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).