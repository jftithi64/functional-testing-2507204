"""Functional tests for every function in target.py.

For each function the tests cover valid inputs, boundary values, invalid
values and wrong argument types.  Exact exception classes are asserted, with
``match=`` wherever target.py defines the message itself.
"""

import math

import pytest

import target

# ==========================================
# 1. is_adult()
# ==========================================

@pytest.mark.parametrize(
    "age, expected",
    [
        (0, False),
        (1, False),
        (17, False),
        (18, True),
        (19, True),
        (100, True),
        (17.99, False),
        (18.0, True),
        (18.5, True),
    ],
)
def test_is_adult_valid(age, expected):
    assert target.is_adult(age) is expected


@pytest.mark.parametrize("age", [-1, -18, -100, -0.5])
def test_is_adult_negative(age):
    with pytest.raises(ValueError, match="age cannot be negative"):
        target.is_adult(age)


@pytest.mark.parametrize("age", ["18", None, [18]])
def test_is_adult_wrong_type(age):
    with pytest.raises(TypeError):
        target.is_adult(age)


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
        (1, 33.8),
        (36.6, 97.88),
        (-273.15, -459.67),
        # Results are rounded to exactly 2 decimals (not 1, not 3, not none).
        (0.123, 32.22),
        (0.005, 32.01),
        (-0.123, 31.78),
    ],
)
def test_celsius_to_fahrenheit_valid(celsius, expected):
    assert target.celsius_to_fahrenheit(celsius) == expected


@pytest.mark.parametrize("celsius", [0, 37, -40, 36.6, 0.123])
def test_celsius_to_fahrenheit_result_type(celsius):
    assert isinstance(target.celsius_to_fahrenheit(celsius), float)


def test_celsius_to_fahrenheit_infinity():
    assert target.celsius_to_fahrenheit(float("inf")) == float("inf")
    assert target.celsius_to_fahrenheit(float("-inf")) == float("-inf")


@pytest.mark.parametrize("celsius", ["abc", "5", None, []])
def test_celsius_to_fahrenheit_wrong_type(celsius):
    with pytest.raises(TypeError):
        target.celsius_to_fahrenheit(celsius)


# ==========================================
# 3. count_vowels()
# ==========================================

@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello", 2),
        ("PYTHON", 1),
        ("AEIOU", 5),
        ("aeiou", 5),
        ("aAeEiIoOuU", 10),
        ("xyz", 0),
        ("rhythm", 0),
        ("y", 0),
        ("", 0),
        ("   ", 0),
        ("Education", 5),
        ("Hello, World! 123", 3),
        ("\n\taeiou", 5),
        ("Python Programming", 4),
        ("caf\u00e9", 1),  # the accented e is not one of a, e, i, o, u
        ("a" * 1000, 1000),
    ],
)
def test_count_vowels_valid(text, expected):
    assert target.count_vowels(text) == expected


@pytest.mark.parametrize("text", [123, 1.5, None, ["a"], b"abc", True])
def test_count_vowels_wrong_type(text):
    with pytest.raises(TypeError, match="text must be a string"):
        target.count_vowels(text)


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
    result = target.invert(flag)
    assert result is expected
    assert type(result) is bool


@pytest.mark.parametrize("value", [1, 0, "True", "", None, [], 1.5])
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
        ("\t\n", "Hello, Guest!"),
        ("Tithi", "Hello, Tithi!"),
        ("  Tithi  ", "Hello, Tithi!"),
        ("\nTithi\t", "Hello, Tithi!"),
        ("Mary Ann", "Hello, Mary Ann!"),
        ("A", "Hello, A!"),
    ],
)
def test_greet_valid(name, expected):
    assert target.greet(name) == expected


def test_greet_default_argument():
    assert target.greet() == "Hello, Guest!"


def test_greet_keyword_argument():
    assert target.greet(name="Sam") == "Hello, Sam!"


# target.py does not validate the type; it fails on .strip() (see README).
@pytest.mark.parametrize("name", [123, 0, 1.5, [], True])
def test_greet_wrong_type(name):
    with pytest.raises(AttributeError, match="strip"):
        target.greet(name)


# ==========================================
# 6. find_max()
# ==========================================

@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 2, 3], 3),
        ([3, 2, 1], 3),
        ([2, 9, 4], 9),
        ([-10, -5, -20], -5),
        ([0], 0),
        ([5, 5, 5], 5),
        ([1.5, 3.7, 2.1], 3.7),
        ([1, 2.5, 2], 2.5),
        ([-1.5, -2.5], -1.5),
        ((3, 1, 2), 3),
        ([10**20, 1], 10**20),
    ],
)
def test_find_max_valid(numbers, expected):
    assert target.find_max(numbers) == expected


@pytest.mark.parametrize("numbers", [[], ()])
def test_find_max_empty(numbers):
    with pytest.raises(ValueError, match="list is empty"):
        target.find_max(numbers)


@pytest.mark.parametrize("numbers", [None, 5, 1.5])
def test_find_max_wrong_type(numbers):
    with pytest.raises(TypeError):
        target.find_max(numbers)


def test_find_max_mixed_element_types():
    with pytest.raises(TypeError):
        target.find_max([1, "a"])


# ==========================================
# 7. get_price()
# ==========================================

@pytest.mark.parametrize(
    "prices, item, expected",
    [
        ({"apple": 50, "banana": 30}, "apple", 50),
        ({"apple": 50, "banana": 30}, "banana", 30),
        ({"item": 0}, "item", 0),
        ({"pen": 1.5}, "pen", 1.5),
        ({"x": None}, "x", None),
        ({1: "one"}, 1, "one"),
        ({"": 7}, "", 7),
    ],
)
def test_get_price_valid(prices, item, expected):
    assert target.get_price(prices, item) == expected


def test_get_price_missing():
    with pytest.raises(KeyError, match="orange not found"):
        target.get_price({"apple": 50}, "orange")


def test_get_price_empty():
    with pytest.raises(KeyError, match="apple not found"):
        target.get_price({}, "apple")


def test_get_price_is_case_sensitive():
    with pytest.raises(KeyError, match="Apple not found"):
        target.get_price({"apple": 50}, "Apple")


@pytest.mark.parametrize("prices", [None, 5])
def test_get_price_wrong_type(prices):
    with pytest.raises(TypeError):
        target.get_price(prices, "apple")


def test_get_price_unhashable_item():
    with pytest.raises(TypeError):
        target.get_price({"apple": 50}, ["apple"])


# ==========================================
# 8. swap()
# ==========================================

@pytest.mark.parametrize(
    "pair, expected",
    [
        ((1, 2), (2, 1)),
        (("hello", "world"), ("world", "hello")),
        ((None, 5), (5, None)),
        ((1, 1), (1, 1)),
        (([1], [2]), ([2], [1])),
        ([1, 2], (2, 1)),
        ("ab", ("b", "a")),
    ],
)
def test_swap_valid(pair, expected):
    result = target.swap(pair)
    assert result == expected
    assert isinstance(result, tuple)


@pytest.mark.parametrize("pair", [(), (1,), (1, 2, 3), [], [1], "abc"])
def test_swap_invalid_length(pair):
    with pytest.raises(ValueError, match="pair must have exactly 2 values"):
        target.swap(pair)


@pytest.mark.parametrize("pair", [123, None, 1.5])
def test_swap_wrong_type(pair):
    with pytest.raises(TypeError):
        target.swap(pair)


# ==========================================
# 9. common_items()
# ==========================================

@pytest.mark.parametrize(
    "set_a, set_b, expected",
    [
        ({1, 2, 3}, {2, 3, 4}, {2, 3}),
        ({1, 2}, {3, 4}, set()),
        (set(), {1, 2}, set()),
        ({1, 2}, set(), set()),
        (set(), set(), set()),
        ({1, 2}, {1, 2}, {1, 2}),
        ({1, 2, 3}, {3}, {3}),
        ({"apple", "banana"}, {"banana", "orange"}, {"banana"}),
        ({1, "a"}, {"a", 2}, {"a"}),
    ],
)
def test_common_items_valid(set_a, set_b, expected):
    result = target.common_items(set_a, set_b)
    assert result == expected
    assert isinstance(result, set)


def test_common_items_does_not_modify_inputs():
    set_a, set_b = {1, 2, 3}, {2, 3, 4}
    target.common_items(set_a, set_b)
    assert set_a == {1, 2, 3}
    assert set_b == {2, 3, 4}


@pytest.mark.parametrize(
    "set_a, set_b",
    [([1, 2], [2, 3]), ({1}, [1]), (None, None), ("ab", "bc")],
)
def test_common_items_wrong_type(set_a, set_b):
    with pytest.raises(TypeError):
        target.common_items(set_a, set_b)


# ==========================================
# 10. is_leap_year()
# ==========================================

@pytest.mark.parametrize(
    "year, expected",
    [
        (1, False),
        (2, False),
        (3, False),
        (4, True),
        (6, False),
        (8, True),
        (100, False),
        (200, False),
        (300, False),
        (400, True),
        (1600, True),
        (1700, False),
        (1800, False),
        (1900, False),
        (1996, True),
        (2000, True),
        (2020, True),
        (2022, False),
        (2023, False),
        (2024, True),
        (2026, False),
        (2100, False),
        (2400, True),
        (9999, False),
        (10000, True),
    ],
)
def test_is_leap_year_valid(year, expected):
    result = target.is_leap_year(year)
    assert result is expected
    assert isinstance(result, bool)


@pytest.mark.parametrize("year", [0, -1, -100, -400, 0.5])
def test_is_leap_year_invalid(year):
    with pytest.raises(ValueError, match="year must be 1 or more"):
        target.is_leap_year(year)


@pytest.mark.parametrize("year", ["2024", None, [2024]])
def test_is_leap_year_wrong_type(year):
    with pytest.raises(TypeError):
        target.is_leap_year(year)


# ==========================================
# 11. to_int()
# ==========================================

@pytest.mark.parametrize(
    "value, expected",
    [
        (10, 10),
        (0, 0),
        (-7, -7),
        (10.9, 10),
        (10.1, 10),
        (-10.9, -10),  # truncates toward zero (not floor, not round)
        (-0.5, 0),
        (1e3, 1000),
        ("123", 123),
        ("-45", -45),
        ("+5", 5),
        ("007", 7),
        ("-0", 0),
        (" 25 ", 25),
        ("  -7\n", -7),
        ("9" * 30, int("9" * 30)),
    ],
)
def test_to_int_valid(value, expected):
    result = target.to_int(value)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("value", [True, False])
def test_to_int_boolean(value):
    with pytest.raises(TypeError, match="bool is not allowed"):
        target.to_int(value)


@pytest.mark.parametrize(
    "value", ["abc", "12.5", "", "  ", "1e3", "0x10", "--5", "1 2", float("nan")]
)
def test_to_int_invalid_value(value):
    with pytest.raises(ValueError):
        target.to_int(value)


def test_to_int_infinity():
    with pytest.raises(OverflowError):
        target.to_int(float("inf"))


@pytest.mark.parametrize("value", [None, [], [1], {}, (1,), 1 + 2j])
def test_to_int_wrong_type(value):
    with pytest.raises(TypeError):
        target.to_int(value)


# ==========================================
# 12. divide()
# ==========================================

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5),
        (10, -2, -5),
        (-10, -2, 5),
        (0, 5, 0),
        (0, -5, 0),
        (5, 1, 5),
        (7.5, 2.5, 3),
        (7, 2, 3.5),
        (-7, 2, -3.5),
        (1, 4, 0.25),
        (1e10, 1e5, 1e5),
    ],
)
def test_divide_valid(a, b, expected):
    assert target.divide(a, b) == expected


@pytest.mark.parametrize("a, b", [(4, 2), (7, 2), (0, 3), (1.5, 0.5)])
def test_divide_result_is_float(a, b):
    assert isinstance(target.divide(a, b), float)


def test_divide_inexact_result():
    assert target.divide(1, 3) == pytest.approx(1 / 3)
    assert target.divide(2, 3) == pytest.approx(2 / 3)


@pytest.mark.parametrize("a, b", [(10, 0), (0, 0), (10, 0.0), (-5, 0), (1.5, 0)])
def test_divide_by_zero(a, b):
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        target.divide(a, b)


@pytest.mark.parametrize(
    "a, b", [("10", 2), (10, "2"), (None, 1), (1, None), ([], 1), (1, [])]
)
def test_divide_wrong_type(a, b):
    with pytest.raises(TypeError):
        target.divide(a, b)


# ==========================================
# 13. power()
# ==========================================

@pytest.mark.parametrize(
    "base, exponent, expected",
    [
        (2, 3, 8),
        (5, 2, 25),
        (2, 10, 1024),
        (10, 0, 1),
        (5, 0, 1),
        (0, 0, 1),
        (0, 3, 0),
        (1, 1000, 1),
        (-2, 3, -8),
        (-2, 2, 4),
        (-1, 3, -1),
        (2, -2, 0.25),
        (2, -1, 0.5),
        (-2, -3, -0.125),
        (1.5, 2, 2.25),
        (0.5, 2, 0.25),
        (4, 0.5, 2.0),
        (2, 100, 1267650600228229401496703205376),
    ],
)
def test_power_valid(base, exponent, expected):
    assert target.power(base, exponent) == expected


def test_power_result_types():
    assert type(target.power(2, 3)) is int
    assert type(target.power(2, -1)) is float
    assert type(target.power(2.0, 3)) is float


def test_power_inexact_result():
    assert target.power(2, 0.5) == pytest.approx(2 ** 0.5)
    assert target.power(10, -2) == pytest.approx(0.01)


def test_power_zero_to_negative_exponent():
    with pytest.raises(ZeroDivisionError, match="negative power"):
        target.power(0, -1)


# target.py does not guard this: a negative base with a fractional exponent
# returns a complex number (see README, suspected bugs).
def test_power_negative_base_fractional_exponent_is_complex():
    assert isinstance(target.power(-8, 0.5), complex)


@pytest.mark.parametrize(
    "base, exponent", [("2", 3), (2, "3"), (None, 2), (2, None), ([], 2)]
)
def test_power_wrong_type(base, exponent):
    with pytest.raises(TypeError):
        target.power(base, exponent)


# ==========================================
# 14. square_root()
# ==========================================

@pytest.mark.parametrize(
    "number, expected",
    [
        (0, 0),
        (0.0, 0),
        (1, 1),
        (4, 2),
        (9, 3),
        (100, 10),
        (2.25, 1.5),
        (0.25, 0.5),
        (1e10, 1e5),
    ],
)
def test_square_root_valid(number, expected):
    result = target.square_root(number)
    assert result == expected
    assert isinstance(result, float)


def test_square_root_inexact_result():
    assert target.square_root(2) == pytest.approx(2 ** 0.5)
    assert target.square_root(1e-10) == pytest.approx(1e-5)


@pytest.mark.parametrize("number", [-1, -4, -0.0001, -1e-9])
def test_square_root_negative(number):
    with pytest.raises(
        ValueError,
        match="cannot take the square root of a negative number"
    ):
        target.square_root(number)


def test_square_root_special_floats():
    assert target.square_root(float("inf")) == float("inf")
    # target.py does not reject NaN; it simply passes it through.
    assert math.isnan(target.square_root(float("nan")))


@pytest.mark.parametrize("number", ["9", None, []])
def test_square_root_wrong_type(number):
    with pytest.raises(TypeError):
        target.square_root(number)


# ==========================================
# 15. factorial()
# ==========================================

@pytest.mark.parametrize(
    "number, expected",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (10, 3628800),
        (12, 479001600),
        (20, 2432902008176640000),
        (25, 15511210043330985984000000),
    ],
)
def test_factorial_valid(number, expected):
    result = target.factorial(number)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("number", [-1, -5, -100])
def test_factorial_negative(number):
    with pytest.raises(
        ValueError,
        match="factorial is not defined for negative numbers"
    ):
        target.factorial(number)


@pytest.mark.parametrize("number", [2.5, 5.0, "5", None, [5]])
def test_factorial_wrong_type(number):
    with pytest.raises(TypeError):
        target.factorial(number)


# ==========================================
# 16. average()
# ==========================================

@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 2, 3], 2),
        ([10, 20, 30], 20),
        ([-10, -20, -30], -20),
        ([5], 5),
        ([7], 7),
        ([0, 0, 0], 0),
        ([1, 2, 3, 4], 2.5),
        ([-1, 1], 0),
        ([2.5, 3.5], 3),
        ([1e10, 1e10], 1e10),
        ((1, 2, 3), 2),
    ],
)
def test_average_valid(numbers, expected):
    result = target.average(numbers)
    assert result == expected
    assert isinstance(result, float)


def test_average_inexact_result():
    assert target.average([1, 2]) == pytest.approx(1.5)
    assert target.average([0.1, 0.2, 0.3]) == pytest.approx(0.2)
    assert target.average([1, 1, 2]) == pytest.approx(4 / 3)


@pytest.mark.parametrize("numbers", [[], ()])
def test_average_empty_list(numbers):
    with pytest.raises(ValueError, match="list is empty"):
        target.average(numbers)


@pytest.mark.parametrize("numbers", [None, 5, 1.5, (n for n in [1, 2])])
def test_average_wrong_type(numbers):
    with pytest.raises(TypeError):
        target.average(numbers)


@pytest.mark.parametrize("numbers", [["a", "b"], [1, "2"]])
def test_average_non_numeric_items(numbers):
    with pytest.raises(TypeError):
        target.average(numbers)

