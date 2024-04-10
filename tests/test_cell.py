import pytest
from src.main import Cell

def test_cell_initialization():
    cell = Cell("A1", "5")
    assert cell.name == "A1"
    assert cell.expression == "5"
    assert cell.resolved is False