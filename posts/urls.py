from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, LikeViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('likes', LikeViewSet, basename='like')

urlpatterns = [
    path('api/', include(router.urls)),
]
