## Task
This is a Python command-line script that takes in a CSV file and processes each cell using Reverse Polish Notation.

## Running the script
python src/main.py input.csv

## Tests
python -m pytest

## Solution Overview
# Cell Class
- Represents individual cells in a spreadsheet
- Attributes:
    - name: The cell identifier i.e 'A1'
    - expression: The content of the cell, which can be a value, an expression, or a reference to another cell.
    - resolved: A boolean indicating whether the cell's expression has been resolved to a value.

# Spreadsheet Class
- Represents individual cells in a spreadsheet
- Attributes:
    - Operators for basic arithmetic operations
- Calculate method: Evaluates an RPN expression represented as a list of tokens and returns the result.

# Calculator Class
- Performs arithmetic calculations, especially for expressions in RPN.
- Methods:
    - calculate(tokens): Evaluates an RPN expression represented as a list of tokens and returns the result.

# CSVProcesser Class
- Facilitates reading from and writing to CSV files.
- Method:
    - parse_csv(): Parses the input CSV file, populates the spreadsheet, resolves expressions, and prepares data for output.
    - write_csv(data): Writes the resolved spreadsheet data to an output CSV file.

The input and output:
- Input CSV: Each cell in the input CSV can contain either a numeric value, arithmetic expression in Reverse Polish Notation or a reference to another cell, i.e A1, A2 etc
- Output CSV: The evaluated spreadsheet is saved to an output CSV file where each cell either contains the correctly calculated value or '#ERR'

## Error Handling
- The script includes error handling for the following issues:
- Unresolvable cell references are left as is or marked with an error code.
- Circular references/loops are detected and prevented from causing infinite loops.
- Invalid expressions result in cells being marked with an error code.

## Nice to have/ Limitations
- Operations currently limited to basic arithmetic and deeply nested references may cause stack errors
- Script has not been tested for csvs in excess of a million rows and performance may degrade
- More thorough testing cases, acceptance tests