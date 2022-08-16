from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path("", include("users.urls")),
    path("auth/token-refresh/", refresh_jwt_token),
    path("mazes", include("mazes.urls"))
]
