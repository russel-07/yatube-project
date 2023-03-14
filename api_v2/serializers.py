from rest_framework.serializers import ModelSerializer, ReadOnlyField
from posts.models import Post


class PostSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date')

