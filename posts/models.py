from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

from users.models import CustomUser

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked '{self.post.title}'"

    class Meta:
        unique_together = ('user', 'post')

    def save(self, *args, **kwargs):
        # Increment the likes_count when a like is added
        self.post.likes_count = F('likes_count') + 1
        self.post.save(update_fields=['likes_count'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement the likes_count when a like is removed
        self.post.likes_count = F('likes_count') - 1
        self.post.save(update_fields=['likes_count'])
        super().delete(*args, **kwargs)
