from django.contrib.auth import get_user_model
from rest_framework import pagination, permissions, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import LikeFilter, PostFilter
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer

User = get_user_model()


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Post.objects.all().order_by('id')
    filterset_class = PostFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['get'], url_path='my-posts', url_name='my_posts')
    def list_posts_by_user(self, request):
        """
        API to list only the posts of the authenticated user.
        """
        user = request.user
        posts = Post.objects.filter(user=user).order_by('id')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    pagination_class = CustomPageNumberPagination
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
    def list_likes_by_user(self, request):
        """
        API to list only the likes of the authenticated user.
        """
        user = request.user
        likes = Like.objects.filter(user=user).order_by('id')
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)
