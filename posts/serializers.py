from rest_framework import serializers

from .models import Post, Tag, Like


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    tags_display = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True, source='tags')
    likes_count = serializers.IntegerField(read_only=True)
    user_name = serializers.SlugRelatedField(slug_field='username', read_only=True, source='user')

    class Meta:
        model = Post
        fields = ['id', 'user_name', 'title', 'description', 'tags', 'tags_display', 'published', 'created_at', 'likes_count']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data, user=self.context['request'].user)
        self.handle_tags(post, tags_data)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            self.handle_tags(instance, tags_data)
        return super().update(instance, validated_data)

    def handle_tags(self, post, tags):
        tag_instances = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_instances.append(tag)
        post.tags.set(tag_instances)


class LikeSerializer(serializers.ModelSerializer):
    post_title = serializers.SlugRelatedField(slug_field='title', read_only=True, source='post')
    user_name = serializers.SlugRelatedField(slug_field='username', read_only=True, source='user')
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'user_name', 'post', 'post_title']

    def validate(self, data):
        user = self.context['request'].user
        post = data['post']
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("You have already liked this post.")
        return data
