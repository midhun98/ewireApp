from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .filters import LikeFilter
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Post.objects.all().order_by('id')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [permission() for permission in self.permission_classes]


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Like.objects.all().order_by('id')
    filterset_class = LikeFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-likes', url_name='my_likes')
    def list_likes_by_user(self, request, user_id=None):
        """
        API to list only the likes of the authenticated user.
        """
        user = request.user
        likes = Like.objects.filter(user=user).order_by('id')
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)