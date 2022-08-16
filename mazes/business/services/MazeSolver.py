from rest_framework.exceptions import ValidationError

from mazes.utils import col_as_index, row_as_index, as_cell_coordinates


class MazeSolver:

    @staticmethod
    def solve_bfs(entrance_coordinates, walls, rows_size, cols_size):
        queue = [entrance_coordinates]
        visited = set()
        exit_coordinates = None
        while queue:
            cell_coordinates = queue.pop(0)
            visited.add(cell_coordinates)
            (row, col) = [
                col_as_index(item) if index == 1 else row_as_index(item)
                for index, item in enumerate(cell_coordinates)
            ]
            if row == rows_size - 1:
                if exit_coordinates and exit_coordinates != cell_coordinates:
                    raise ValueError('Maze has more than one exit')
                exit_coordinates = cell_coordinates
            if MazeSolver._is_safe(walls, visited, row + 1, col, rows_size, cols_size):
                queue.append(as_cell_coordinates(row + 1, col))
            if MazeSolver._is_safe(walls, visited, row - 1, col, rows_size, cols_size):
                queue.append(as_cell_coordinates(row - 1, col))
            if MazeSolver._is_safe(walls, visited, row, col + 1, rows_size, cols_size):
                queue.append(as_cell_coordinates(row, col + 1))
            if MazeSolver._is_safe(walls, visited, row, col - 1, rows_size, cols_size):
                queue.append(as_cell_coordinates(row, col - 1))

    @staticmethod
    def solve_maze_dfs(entrance_coordinates, walls, rows_size, cols_size):
        paths = []
        exit_coordinates = []
        MazeSolver.solve_maze_dfs_rec(entrance_coordinates, walls, rows_size, cols_size, [], exit_coordinates, paths)
        return exit_coordinates[0] if exit_coordinates else None, paths

    @staticmethod
    def solve_maze_dfs_rec(
            cell_coordinates,
            walls,
            rows_size,
            cols_size,
            visited,
            exit_coordinates,
            paths
    ):
        (row, col) = [
            col_as_index(item) if index == 1 else row_as_index(item)
            for index, item in enumerate(cell_coordinates)
        ]

        visited.append(cell_coordinates)

        if row == rows_size - 1:
            if exit_coordinates and exit_coordinates[0] != cell_coordinates:
                raise ValidationError('Maze has more than one exit')
            exit_coordinates.append(cell_coordinates)
            paths.append(visited.copy())

        for next_row, next_col in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if MazeSolver._is_safe(walls, visited, next_row, next_col, rows_size, cols_size):
                next_cell_coordinates = as_cell_coordinates(next_row, next_col)
                MazeSolver.solve_maze_dfs_rec(
                    next_cell_coordinates,
                    walls,
                    rows_size,
                    cols_size,
                    visited,
                    exit_coordinates,
                    paths
                )

        visited.pop()

    @staticmethod
    def _is_safe(walls, visited, row, col, rows_size, cols_size):
        if ((0 <= row < rows_size)
                and (0 <= col < cols_size)
                and as_cell_coordinates(row, col) not in walls
                and as_cell_coordinates(row, col) not in visited
        ):
            return True
        return False