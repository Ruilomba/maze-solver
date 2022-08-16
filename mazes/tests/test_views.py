import json

from django.test import TestCase, Client
from rest_framework import status

from mazes.models import Maze
from users.serializers import UserRegistrationSerializer

client = Client()


class MazeCreationTest(TestCase):
    def setUp(self):
        self.username = "rui"
        data = {
            "email": f"{self.username}@test.com",
            "password": self.username,
            "profile": {"name": self.username},
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "email": f"{self.username}@test.com",
            "password": {self.username},
        }
        response = client.post(path="/login", data=data)
        self.token = response.data["token"]

    def test_maze_creation_invalid_token(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token} + 2asds"
        }
        data = {
            'gridSize': '8xs',
            'entrance': 'A1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 401)

    def test_maze_creation_invalid_grid_size_no_col(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8xs',
            'entrance': 'A1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'gridSize parameter must be a string with format row_numberxcol_number e.g. 8x8 and got 8xs',
            str(response.data[0]))

    def test_maze_creation_invalid_grid_size_string_after_col(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8x8x',
            'entrance': 'A1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'gridSize parameter must be a string with format row_numberxcol_number e.g. 8x8 and got 8x8x',
            str(response.data[0]))

    def test_maze_creation_invalid_grid_size_string_before_col(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': 'x8x8',
            'entrance': 'A1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'gridSize parameter must be a string with format row_numberxcol_number e.g. 8x8 and got x8x8',
            str(response.data[0]))

    def test_maze_creation_invalid_entrance_outside_grid(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8x8',
            'entrance': 'M1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'Coordinates M1 are outside maze',
            str(response.data[0]))

    def test_maze_creation_invalid_entrance_invalid_format(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8x8',
            'entrance': 'Ms1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'Cell coordinates should be described as [A-Z][1-9]+',
            str(response.data[0]))

    def test_maze_creation_invalid_walls_outside_grid(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8x8',
            'entrance': 'A1',
            'walls': ['M2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'Coordinates M2 are outside maze',
            str(response.data[0]))

    def test_maze_creation_invalid_walls_invalid_format(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8x8',
            'entrance': 'A1',
            'walls': ['As2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'Cell coordinates should be described as [A-Z][1-9]+',
            str(response.data[0]))

    def test_maze_creation_more_than_one_exit(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'gridSize': '8x8',
            'entrance': 'A1',
            'walls': ['A2', 'A3']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            'Maze has more than one exit',
            str(response.data[0]))

    def test_maze_creation(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'entrance': 'A1',
            'gridSize': '8x8',
            'walls': ['G1', 'H1', 'A2', 'C2', 'E2', 'H2', 'G2', 'C3',
                      'E3', 'H3', 'B4', 'C4', 'E4', 'F4', 'B5', 'E5', 'H5', 'B6', 'D6',
                      'E6', 'G6', 'H6', 'B7', 'D7', 'G7', 'H7', 'B8', 'H8']
        }
        response = client.post(path="/mazes", data=data, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        maze = Maze.objects.get(id=response.data['id'])
        self.assertEqual(
            ['A1', 'B1', 'C1', 'D1', 'D2', 'D3', 'D4', 'D5', 'C5', 'C6', 'C7',
             'C8', 'D8', 'E8', 'F8', 'F7', 'F6', 'F5', 'G5', 'G4', 'H4'],
            maze.max_path
        )
        self.assertEqual(
            ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'F2', 'F3', 'G3', 'G4', 'H4'],
            maze.min_path
        )
        self.assertEqual('H4', maze.exit_coordinates)
        self.assertEqual('A1', maze.entrance)
        self.assertEqual('rui@test.com', maze.user.email)
        self.assertEqual('8x8', maze.grid_size)
        self.assertEqual(
            ['G1', 'H1', 'A2', 'C2', 'E2', 'H2', 'G2', 'C3',
             'E3', 'H3', 'B4', 'C4', 'E4', 'F4', 'B5', 'E5', 'H5', 'B6', 'D6',
             'E6', 'G6', 'H6', 'B7', 'D7', 'G7', 'H7', 'B8', 'H8'],
            maze.walls
        )


class MazeSolutionTestCase(TestCase):
    def setUp(self):
        self.username = "rui"
        data = {
            "email": f"{self.username}@test.com",
            "password": self.username,
            "profile": {"name": self.username},
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.user = serializer.save()
        data = {
            "email": f"{self.username}@test.com",
            "password": {self.username},
        }
        response = client.post(path="/login", data=data)
        self.token = response.data["token"]

    def test_get_solution_no_permission_for_maze(self):
        username = 'another_user'
        data = {
            "email": f"{username}@test.com",
            "password": username,
            "profile": {"name": self.username},
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        maze = self._build_maze(user)
        maze.save()
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'steps': 'min'
        }
        response = client.get(path=f'/mazes/{maze.id}/solution', data=data, **headers)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_solution_min_path_default(self):
        maze = self._build_maze(self.user)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {}
        response = client.get(path=f'/mazes/{maze.id}/solution', data=data, **headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'F2', 'F3', 'G3', 'G4', 'H4'],
            response.data['min_path']
        )

    def test_get_solution_min_path(self):
        maze = self._build_maze(self.user)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'steps': 'min'
        }
        response = client.get(path=f'/mazes/{maze.id}/solution', data=data, **headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'F2', 'F3', 'G3', 'G4', 'H4'],
            response.data['min_path']
        )

    def test_get_solution_max_path(self):
        maze = self._build_maze(self.user)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}"
        }
        data = {
            'steps': 'max'
        }
        response = client.get(path=f'/mazes/{maze.id}/solution', data=data, **headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            ['A1', 'B1', 'C1', 'D1', 'D2', 'D3', 'D4', 'D5', 'C5', 'C6', 'C7',
             'C8', 'D8', 'E8', 'F8', 'F7', 'F6', 'F5', 'G5', 'G4', 'H4'],
            response.data['max_path']
        )

    def _build_maze(self, user):
        maze = Maze()
        maze.walls = []
        maze.entrance = 'A1'
        maze.grid_size = '8x8'
        maze.walls = ['G1', 'H1', 'A2', 'C2', 'E2', 'H2', 'G2', 'C3',
                      'E3', 'H3', 'B4', 'C4', 'E4', 'F4', 'B5', 'E5', 'H5', 'B6', 'D6',
                      'E6', 'G6', 'H6', 'B7', 'D7', 'G7', 'H7', 'B8', 'H8']
        maze.user = user
        maze.save()
        return maze
