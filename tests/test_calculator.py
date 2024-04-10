import pytest
from src.main import Calculator

@pytest.fixture
def calculator():
    return Calculator()

def test_addition(calculator):
    result = calculator.calculate(['2', '3', '+'])
    assert result == 5

def test_float_calculation(calculator):
    result = calculator.calculate(['4', '40', '/', '-1', '+'])
    assert result == -0.9

def test_subtraction(calculator):
    result = calculator.calculate(['5', '3', '-'])
    assert result == 2

def test_multiplication(calculator):
    result = calculator.calculate(['4', '3', '*'])
    assert result == 12

def test_division(calculator):
    result = calculator.calculate(['10', '2', '/'])
    assert result == 5

def test_complex_expression(calculator):
    result = calculator.calculate(['2', '3', '+', '4', '*', '6', '/'])
    assert result == 3.33
