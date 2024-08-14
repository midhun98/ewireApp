from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.LoginAPI.as_view(), name='login-api'), # API  to login a user
    path('api/register/', views.UserRegistrationView.as_view(), name='register'),  # API  to create a new user
]