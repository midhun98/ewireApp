from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.LoginAPI.as_view(), name='login-api'),
]