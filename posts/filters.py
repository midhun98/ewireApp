import django_filters
from .models import Like, Post


class LikeFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Like
        fields = ['user_id']


class PostFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    user_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Post
        fields = ['description', 'title', 'user_id']
