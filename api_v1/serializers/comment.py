from rest_framework import serializers
from webapp.models.comments import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'post', 'author']