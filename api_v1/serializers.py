from rest_framework.serializers import ModelSerializer, ReadOnlyField
from posts.models import Post, Comment


class PostSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date')


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    post = ReadOnlyField(source='post.id')
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')