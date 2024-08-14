from django.contrib import admin

from .models import Post, Tag, Like


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'published', 'likes_count')
    filter_horizontal = ('tags',)


admin.site.register(Tag)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
