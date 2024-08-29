from rest_framework import serializers
from webapp.models import Post
from rest_framework.serializers import ModelSerializer
from webapp.models import Comment


class PostSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = Post
        fields = ['id', 'image', 'summary', 'likes_count', 'comments_count', 'author', 'created_at', 'liked_by']
        read_only_fields = ['id', 'created_at', 'author', 'comments_count']

