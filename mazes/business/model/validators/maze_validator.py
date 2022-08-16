from rest_framework.exceptions import ValidationError

from mazes.business.model.maze import Maze
from mazes.utils import col_as_index, row_as_index


def validate_maze(grid_size, walls, entrance):
    grid_size_match = Maze.GRID_SIZE_PATTERN.match(grid_size)
    if not grid_size_match:
        raise ValidationError(
            f'gridSize parameter must be a string with '
            f'format row_numberxcol_number e.g. 8x8 and got {grid_size}'
        )
    (rows_size, cols_size) = [int(x) for x in grid_size_match.groups()]
    [_validate_cell_pattern(x) for x in walls + [entrance]]
    [_validate_boundaries(x, rows_size, cols_size) for x in walls + [entrance]]


def _validate_boundaries(cell_coordinates, rows_size, cols_size):
    (entrance_row, entrance_col) = [
        col_as_index(item) if index == 1 else row_as_index(item)
        for index, item in enumerate(cell_coordinates)
    ]

    if entrance_row >= rows_size or entrance_col >= cols_size:
        raise ValidationError(f'Coordinates {cell_coordinates} are outside maze')


def _validate_cell_pattern(cell_coordinate):
    cell_coordinate_match = Maze.CELL_PATTERN.match(cell_coordinate)
    if not cell_coordinate_match:
        raise ValidationError(f'Cell coordinates should be described as [A-Z][1-9]+')