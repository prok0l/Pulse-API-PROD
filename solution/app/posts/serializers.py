from rest_framework import serializers

from user.models import UserModel
from .models import Post, Reactions


class NewPostSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)
    tags = serializers.ListSerializer(
        child=serializers.CharField(max_length=20))
    author = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all())

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class ViewPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.login')
    likesCount = serializers.SerializerMethodField()
    dislikesCount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "content", "author", "createdAt", "tags",
                  "likesCount", "dislikesCount")

    @staticmethod
    def get_likesCount(obj):
        return Reactions.objects.filter(post=obj, positive=True).count()

    @staticmethod
    def get_dislikesCount(obj):
        return Reactions.objects.filter(post=obj, positive=False).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['createdAt'] = instance.createdAt.strftime('%Y-%m-%dT%H:%M:%SZ')
        return data
