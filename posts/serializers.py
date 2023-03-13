from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    read_only_field = ['author']
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date')