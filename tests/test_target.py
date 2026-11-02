
import pytest

import target

# ==========================================
# 1. is_adult()
# ==========================================

@pytest.mark.parametrize(
    "age, expected",
    [
        (0, False),
        (17, False),
        (18, True),
        (19, True),
        (100, True),
    ],
)
def test_is_adult_valid(age, expected):
    assert target.is_adult(age) is expected


def test_is_adult_negative():
    with pytest.raises(ValueError, match="age cannot be negative"):
        target.is_adult(-1)


def test_is_adult_wrong_type():
    with pytest.raises(TypeError):
        target.is_adult("18")


# ==========================================
# 2. celsius_to_fahrenheit()
# ==========================================

@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0),
        (100, 212.0),
        (-40, -40.0),
        (37, 98.6),
        (25, 77.0),
    ],
)
def test_celsius_to_fahrenheit_valid(celsius, expected):
    assert target.celsius_to_fahrenheit(celsius) == expected


def test_celsius_to_fahrenheit_result_type():
    result = target.celsius_to_fahrenheit(0)
    assert isinstance(result, float)


def test_celsius_to_fahrenheit_wrong_type():
    with pytest.raises(TypeError):
        target.celsius_to_fahrenheit("abc")


# ==========================================
# 3. count_vowels()
# ==========================================

@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello", 2),
        ("PYTHON", 1),
        ("AEIOU", 5),
        ("xyz", 0),
        ("", 0),
        ("Education", 5),
    ],
)
def test_count_vowels_valid(text, expected):
    assert target.count_vowels(text) == expected


def test_count_vowels_wrong_type():
    with pytest.raises(TypeError, match="text must be a string"):
        target.count_vowels(123)


# ==========================================
# 4. invert()
# ==========================================

@pytest.mark.parametrize(
    "flag, expected",
    [
        (True, False),
        (False, True),
    ],
)
def test_invert_valid(flag, expected):
    assert target.invert(flag) is expected


@pytest.mark.parametrize("value", [1, 0, "True", None, [], 1.5])
def test_invert_wrong_type(value):
    with pytest.raises(TypeError, match="flag must be True or False"):
        target.invert(value)


# ==========================================
# 5. greet()
# ==========================================

@pytest.mark.parametrize(
    "name, expected",
    [
        (None, "Hello, Guest!"),
        ("", "Hello, Guest!"),
        ("   ", "Hello, Guest!"),
        ("Tithi", "Hello, Tithi!"),
        ("  Tithi  ", "Hello, Tithi!"),
    ],
)
def test_greet_valid(name, expected):
    assert target.greet(name) == expected


def test_greet_wrong_type():
    with pytest.raises(AttributeError, match="strip"):
        target.greet(123)

# 6. find_max()
@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3], 3),
    ([-10, -5, -20], -5),
    ([0], 0),
    ([5, 5, 5], 5),
    ([1.5, 3.7, 2.1], 3.7),
])
def test_find_max_valid(numbers, expected):
    assert target.find_max(numbers) == expected


def test_find_max_empty():
    with pytest.raises(ValueError, match="list is empty"):
        target.find_max([])


def test_find_max_wrong_type():
    with pytest.raises(TypeError):
        target.find_max(None)


# 7. get_price()
@pytest.mark.parametrize("prices, item, expected", [
    ({"apple": 50, "banana": 30}, "apple", 50),
    ({"apple": 50, "banana": 30}, "banana", 30),
    ({"item": 0}, "item", 0),
])
def test_get_price_valid(prices, item, expected):
    assert target.get_price(prices, item) == expected


def test_get_price_missing():
    with pytest.raises(KeyError, match="orange not found"):
        target.get_price({"apple": 50}, "orange")


def test_get_price_empty():
    with pytest.raises(KeyError):
        target.get_price({}, "apple")


def test_get_price_wrong_type():
    with pytest.raises(TypeError):
        target.get_price(None, "apple")


# 8. swap()
@pytest.mark.parametrize("pair, expected", [
    ((1, 2), (2, 1)),
    (("hello", "world"), ("world", "hello")),
    ((None, 5), (5, None)),
])
def test_swap_valid(pair, expected):
    result = target.swap(pair)
    assert result == expected
    assert isinstance(result, tuple)


@pytest.mark.parametrize("pair", [
    (), (1,), (1, 2, 3)
])
def test_swap_invalid_length(pair):
    with pytest.raises(ValueError, match="pair must have exactly 2 values"):
        target.swap(pair)


def test_swap_wrong_type():
    with pytest.raises(TypeError):
        target.swap(123)


# 9. common_items()
@pytest.mark.parametrize("set_a, set_b, expected", [
    ({1, 2, 3}, {2, 3, 4}, {2, 3}),
    ({1, 2}, {3, 4}, set()),
    (set(), {1, 2}, set()),
    ({"apple", "banana"}, {"banana", "orange"}, {"banana"}),
])
def test_common_items_valid(set_a, set_b, expected):
    result = target.common_items(set_a, set_b)
    assert result == expected
    assert isinstance(result, set)


def test_common_items_wrong_type():
    with pytest.raises(TypeError):
        target.common_items([1, 2], [2, 3])


# 10. is_leap_year()
@pytest.mark.parametrize("year, expected", [
    (2024, True),
    (2023, False),
    (2000, True),
    (1900, False),
    (2020, True),
    (400, True),
    (100, False),
    (1, False),
    (4, True),
])
def test_is_leap_year_valid(year, expected):
    result = target.is_leap_year(year)
    assert result is expected
    assert isinstance(result, bool)


@pytest.mark.parametrize("year", [0, -1, -100])
def test_is_leap_year_invalid(year):
    with pytest.raises(ValueError, match="year must be 1 or more"):
        target.is_leap_year(year)


def test_is_leap_year_wrong_type():
    with pytest.raises(TypeError):
        target.is_leap_year("2024")


# 11. to_int()
@pytest.mark.parametrize("value, expected", [
    (10, 10),
    (10.9, 10),
    ("123", 123),
    ("-45", -45),
    (" 25 ", 25),
    (0, 0),
])
def test_to_int_valid(value, expected):
    result = target.to_int(value)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("value", [True, False])
def test_to_int_boolean(value):
    with pytest.raises(TypeError, match="bool is not allowed"):
        target.to_int(value)


@pytest.mark.parametrize("value", ["abc", "12.5", ""])
def test_to_int_invalid_string(value):
    with pytest.raises(ValueError):
        target.to_int(value)


def test_to_int_none():
    with pytest.raises(TypeError):
        target.to_int(None)

# 12. divide()
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (10, -2, -5),
    (-10, -2, 5),
    (0, 5, 0),
    (7.5, 2.5, 3),
])
def test_divide_valid(a, b, expected):
    assert target.divide(a, b) == expected


def test_divide_inexact_result():
    assert target.divide(1, 3) == pytest.approx(1 / 3)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        target.divide(10, 0)


def test_divide_wrong_type():
    with pytest.raises(TypeError):
        target.divide("10", 2)


# 13. power()
@pytest.mark.parametrize("base, exponent, expected", [
    (2, 3, 8),
    (5, 2, 25),
    (10, 0, 1),
    (2, -2, 0.25),
    (-2, 3, -8),
    (0, 3, 0),
    (0, 0, 1),
])
def test_power_valid(base, exponent, expected):
    assert target.power(base, exponent) == expected


def test_power_inexact_result():
    assert target.power(2, 0.5) == pytest.approx(2 ** 0.5)


def test_power_wrong_type():
    with pytest.raises(TypeError):
        target.power("2", 3)


# 14. square_root()
@pytest.mark.parametrize("number, expected", [
    (0, 0),
    (1, 1),
    (4, 2),
    (9, 3),
    (100, 10),
])
def test_square_root_valid(number, expected):
    result = target.square_root(number)
    assert result == expected
    assert isinstance(result, float)


def test_square_root_inexact_result():
    assert target.square_root(2) == pytest.approx(2 ** 0.5)


def test_square_root_negative():
    with pytest.raises(
        ValueError,
        match="cannot take the square root of a negative number"
    ):
        target.square_root(-4)


def test_square_root_wrong_type():
    with pytest.raises(TypeError):
        target.square_root("9")


# 15. factorial()
@pytest.mark.parametrize("number, expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (5, 120),
    (10, 3628800),
])
def test_factorial_valid(number, expected):
    result = target.factorial(number)
    assert result == expected
    assert isinstance(result, int)


def test_factorial_negative():
    with pytest.raises(
        ValueError,
        match="factorial is not defined for negative numbers"
    ):
        target.factorial(-5)


@pytest.mark.parametrize("number", [2.5, "5", None])
def test_factorial_wrong_type(number):
    with pytest.raises(TypeError):
        target.factorial(number)


# 16. average()
@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3], 2),
    ([10, 20, 30], 20),
    ([-10, -20, -30], -20),
    ([5], 5),
    ([0, 0, 0], 0),
    ([1, 2, 3, 4], 2.5),
])
def test_average_valid(numbers, expected):
    result = target.average(numbers)
    assert result == expected
    assert isinstance(result, float)


def test_average_inexact_result():
    assert target.average([1, 2]) == pytest.approx(1.5)


def test_average_empty_list():
    with pytest.raises(ValueError, match="list is empty"):
        target.average([])


def test_average_wrong_type():
    with pytest.raises(TypeError):
        target.average(None)
