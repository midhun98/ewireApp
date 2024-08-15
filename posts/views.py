from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


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

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)