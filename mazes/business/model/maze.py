import re


class Maze:
    GRID_SIZE_PATTERN = re.compile(r'^([1-9]+)x([1-9]+)$')
    CELL_PATTERN = re.compile(r'^([A-Z])([1-9]+)$')

