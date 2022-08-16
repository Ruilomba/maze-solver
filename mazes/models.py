from django.db import models

from mazes.business.model.validators import maze_validator
from mazes.business.services.MazeSolver import MazeSolver
from users.models import User


class Maze(models.Model):
    grid_size = models.CharField(max_length=20)
    entrance = models.CharField(max_length=20)
    walls = models.JSONField()
    user = models.ForeignKey(User, to_field='email', on_delete=models.CASCADE)
    exit_coordinates = models.CharField(max_length=20, null=True, blank=True)
    min_path = models.JSONField(null=True, blank=True)
    max_path = models.JSONField(null=True, blank=True)

    def clean(self):
        maze_validator.validate_maze(self.grid_size, self.walls, self.entrance)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()

        grid_sizes = self.grid_size.split('x')
        exit_coordinates, paths = MazeSolver.solve_maze_dfs(
            entrance_coordinates=self.entrance,
            walls=self.walls,
            rows_size=int(grid_sizes[0]),
            cols_size=int(grid_sizes[1])
        )

        max_path = None
        min_path = None
        for path in paths:
            if not max_path or len(path) > len(max_path):
                max_path = path
            if not min_path or len(path) < len(min_path):
                min_path = path

        self.min_path = min_path
        self.max_path = max_path
        self.exit_coordinates = exit_coordinates
        return super().save(force_insert, force_update, using, update_fields)

