from rest_framework.serializers import ModelSerializer
from .models import Comment

class CreateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

class PostCommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'slug', 'parent', 'comment_author', 'vote_count', 'date_created', 'replies']

class UpdateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

class CommentRepliesSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'comment_author', 'post', 'parent', 'date_created']