from django.urls import path

from mazes.views import MazeView, MazeSolutionView

urlpatterns = [
    path("", MazeView.as_view()),
    path("/<int:id>/solution", MazeSolutionView.as_view())
]