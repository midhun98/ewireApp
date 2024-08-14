from django.contrib import admin
from django.core.checks import Tags

from .models import Post, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)