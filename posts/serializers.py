from rest_framework.serializers import ModelSerializer
from .models import Post

class CreatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [ 'title', 'content']

class AllPostsSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'vote_count', 'date_created']

class SinglePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'created_by', 'vote_count', 'date_created', 'post_comments']