from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        # build grid as a list of lists containing ints
        self._grid: list[list[int]] = []

        # append puzzle input to grid
        for puzzle_row in puzzle:
            row_list = []
            for element in puzzle_row:
                row_list.append(int(element))

            self._grid.append(row_list)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            # check for 0 in row, if so get y coordinate
            if 0 in self._grid[y]:
                if next_x == -1 and next_y == -1:
                    next_x, next_y = self._grid[y].index(0), y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""

        values = self._grid[i]

        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""

        # gets the ith item of every row in grid
        values = [item[i] for item in self._grid]

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3)
        y_start = (i // 3) * 3

        for y in range(y_start, y_start + 3):
            # splits row into three parts
            row = list(zip(*(iter(self._grid[y]),) * 3))
            # adds values of row split for right block
            values += list(row[x_start])

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = True

        for i in range(9):
            # sudoku not solved if there is a value missing in column values
            if values != sorted(self.column_values(i)):
                result = False

            # sudoku not solved if there is a value missing in row values
            if values != sorted(self.row_values(i)):
                result = False

            # sudoku not solved if there is a value missing in block values
            if values != sorted(self.block_values(i)):
                result = False

        return result

    def __str__(self) -> str:
        representation = ""

        # prints representation of sudoku
        for row in self._grid:
            row2 = " ".join(str(e) for e in row)
            representation += row2 + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
