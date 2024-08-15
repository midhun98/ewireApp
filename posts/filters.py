import django_filters
from .models import Like

class LikeFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Like
        fields = ['user_id']
