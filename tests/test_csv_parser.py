import pytest
import csv
from src.main import CSVProcesser

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        return [row for row in csv.reader(csvfile)]

@pytest.fixture(scope="function")
def setup_files(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    content = "10,2 3 +\n" + "4,5 3 -\n"
    input_file.write_text(content)
    return input_file, output_file

def test_csv_processor_acceptance(setup_files):
    input_file, output_file = setup_files
    processor = CSVProcesser(str(input_file), str(output_file))
    processor.parse_csv()

    expected_output = [["10", "5"], ["4", "2"]]
    output_data = read_csv(output_file)

    assert expected_output == output_data, f"Expected {expected_output}, got {output_data}"
