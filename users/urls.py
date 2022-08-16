from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
)

urlpatterns = [
    path("user", UserRegistrationView.as_view()),
    path("login", UserLoginView.as_view()),
]
