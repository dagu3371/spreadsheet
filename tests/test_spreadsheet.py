import pytest
from src.main import SpreadSheet

@pytest.fixture
def spreadsheet():
    return SpreadSheet()

def test_no_operators_error(spreadsheet):
    result = spreadsheet.no_operators_error(['1', '2'])
    assert result == True

def test_only_operators_error(spreadsheet):
    result = spreadsheet.only_operators_error(['*'])
    assert result == True

def test_ref_loop_error(spreadsheet):
    result = spreadsheet.ref_loop_error(['C1'], 'C1')
    assert result == True

def test_add_cell_to_spreadsheet():
    sheet = SpreadSheet()
    sheet.add_cell("A1", "5")
    assert "a1" in sheet.cell_values
    assert sheet.cell_values["a1"].expression == "5"