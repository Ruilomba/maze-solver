from rest_framework import serializers

from mazes.models import Maze


class MazeSerializer(serializers.ModelSerializer):
    gridSize = serializers.CharField(read_only=True, source='grid_size')

    class Meta:
        model = Maze
        fields = ('id', 'entrance', 'walls', 'user', 'gridSize')


class MazeCreationSerializer(serializers.ModelSerializer):
    gridSize = serializers.CharField(source='grid_size', required=False)

    class Meta:
        model = Maze
        fields = ('entrance', 'walls', 'user', 'gridSize')
