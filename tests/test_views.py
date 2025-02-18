import json
from typing import Any

import pytest

from src.views import location_of_the_main_function


def test_location_of_the_main_function_default_date() -> Any:
    result = location_of_the_main_function()
    assert isinstance(result, str)
    assert json.loads(result)


def test_location_of_the_main_function_custom_date() -> Any:
    date = "2022-01-01 12:00:00"
    result = location_of_the_main_function(date)
    assert isinstance(result, str)
    assert json.loads(result)


def test_location_of_the_main_function_invalid_date() -> Any:
    date = " invalid date "
    with pytest.raises(ValueError):
        location_of_the_main_function(date)


@pytest.mark.parametrize("date, expected", [
    ("2020-10-12 02:10:47", "Доброй ночи"),
    ("2018-05-12 08:40:24", "Доброе утро")
])
def test_location_of_the_main_function_greeting(date: str, expected: str) -> Any:
    result = location_of_the_main_function(date)
    result_dict = json.loads(result)
    assert result_dict["greeting"] == expected
