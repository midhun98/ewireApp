from rest_framework import serializers

from .models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    tags_display = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True, source='tags')

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'tags_display', 'published', 'created_at']

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
