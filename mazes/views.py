from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from mazes.models import Maze
from mazes.serializers import MazeSerializer, MazeCreationSerializer


class MazeView(
    GenericAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = MazeSerializer
    creation_serializer_class = MazeCreationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request, *args, **kwargs):
        serializer = self.creation_serializer_class(data={**request.data, **{'user': request.user.email}})
        serializer.is_valid(raise_exception=True)
        maze = serializer.save()
        return Response({'id': maze.id}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """
        This view should return a list of all the mazes
        for the currently authenticated user.
        """
        user = self.request.user
        return Maze.objects.filter(user__email=user)


class MazeSolutionView(GenericAPIView, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, id):
        steps = request.GET.get('steps', 'min')
        try:
            maze = Maze.objects.get(id=id, user=request.user.email)
        except Maze.DoesNotExist:
            return Response({'Response': 'Not Found'}, status.HTTP_404_NOT_FOUND)

        return Response(
            {'min_path': maze.min_path} if steps == 'min' else {'max_path': maze.max_path},
            status.HTTP_200_OK
        )

