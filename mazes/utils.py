def row_as_index(row_coordinate):
    return ord(row_coordinate) - ord('A')


def col_as_index(col_coordinate):
    return int(col_coordinate) - 1


def as_cell_coordinates(row, col):
    return as_row_coordinate(row) + str(col + 1)


def as_row_coordinate(index):
    return chr(index + ord('A'))


def as_col_coordinate(index):
    return chr(index + 1)
