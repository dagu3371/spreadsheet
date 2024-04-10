import csv
import sys
import os
import operator

class Cell:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.resolved = False

class SpreadSheet:
    def __init__(self):
        self.cell_values = {}
        self.calculator = Calculator()
        self.unresolved_cells = []

    def add_cell(self, cell_name, expression):
        cell = Cell(cell_name, expression)
        self.cell_values[cell_name.lower()] = cell

    def resolve_cell(self, cell):
        if cell.resolved:
            return cell.expression

        resolved_expression = []
        unresolved = False
        for token in cell.expression:
            if str(token).isdigit() or token in self.calculator.ops:
                resolved_expression.append(token)
            else:
                referenced_cell = self.cell_values.get(token.lower())
                if referenced_cell and not referenced_cell.resolved:
                    unresolved = True
                    break
                elif referenced_cell:
                    resolved_value = self.resolve_cell(referenced_cell)
                    resolved_expression.append(resolved_value)
                else:
                    unresolved = True
                    break
        if not unresolved:
                evaluated_result = self.calculator.calculate(resolved_expression)
                cell.expression = evaluated_result
                cell.resolved = True
                return evaluated_result
        else:
            if cell not in self.unresolved_cells:
                self.unresolved_cells.append(cell)
            return None


    def set_cell_value(self, cell, expression):
        cell.expression = expression

    def retry_unresolved_cells(self):
        # Attempt to resolve each unresolved cell again
        previously_unresolved = len(self.unresolved_cells)
        while self.unresolved_cells:
            cell = self.unresolved_cells.pop(0)
            self.resolve_cell(cell)

            # If no progress is made, stop to prevent infinite loop
            if len(self.unresolved_cells) >= previously_unresolved:
                break
            previously_unresolved = len(self.unresolved_cells)

    def populate_spreadsheet(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row_idx, row in enumerate(reader):
                for col_idx, cells in enumerate(row):
                    cell_name = f"{chr(65 + col_idx)}{row_idx + 1}"

                    expression = cells.strip().split(' ')
                    self.add_cell(cell_name, expression)
                    cell = self.cell_values[cell_name.lower()]

                    if self.no_operators_error(expression):
                        self.set_cell_value(cell, "#ERR")
                        continue
                    elif self.only_operators_error(expression):
                        self.set_cell_value(cell, "#ERR")
                        continue
                    elif self.ref_loop_error(expression, cell_name):
                        self.set_cell_value(cell, "#ERR")
                        continue
                    else:
                        self.resolve_cell(cell)

    def no_operators_error(self, expression):
        return all(x.isdigit() for x in expression) and len(expression) > 1

    def only_operators_error(self, expression):
        return all(x in ['+', '-', '*', '/'] for x in expression)

    def ref_loop_error(self, expression, cell_name):
        return any(exp.lower() == cell_name.lower() for exp in expression)

class Calculator:
    def __init__(self):
        self.ops = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,
        }

    def calculate(self, tokens):
        nums = []
        for token in tokens:
            if token in self.ops:
                if len(nums) < 2:
                    return '#ERR'
                j = nums.pop()
                k = nums.pop()
                nums.append(self.ops[token](k,j))
            else:
                nums.append(int(token))

        if len(nums) == 1:
            return round(nums[0], 2)
        else:
            return '#ERR'

class CSVProcesser:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def parse_csv(self):
        spreadsheet = SpreadSheet()
        spreadsheet.populate_spreadsheet(self.input_file_path)
        spreadsheet.retry_unresolved_cells()
        self.write_csv(spreadsheet.cell_values)

    def write_csv(self, data):
        num_rows = max(int(key[1:]) for key in data.keys())
        num_cols = max(ord(key[0].lower()) - ord('a') for key in data.keys()) + 1
        grid = [[None for _ in range(num_cols)] for _ in range(num_rows)]

        # Populate the grid with values from the dictionary
        for key, value in data.items():
            col = ord(key[0].lower()) - ord('a')  # Convert column letter to zero-based index
            row = int(key[1:]) - 1  # Convert row number to zero-based index
            grid[row][col] = value.expression

        with open(self.output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in grid:
                writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please pass arguments like so: python src/main.py input.csv")
    else:
        input_file_path = sys.argv[1]
        input_path = os.path.join('src/fixtures', input_file_path)
        output_file_path = os.path.join('src/fixtures', 'output.csv')
        csv_processer = CSVProcesser(input_path, output_file_path)
        csv_processer.parse_csv()