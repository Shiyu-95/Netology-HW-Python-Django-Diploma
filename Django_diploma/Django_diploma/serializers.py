from rest_framework import serializers

from photo_social_network.models import Comment, Post, Like, PostImage


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'post', 'image']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    images = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True,
                                                queryset=PostImage.objects.all())
    place = serializers.CharField(max_length=100)
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'title', 'text', "comments", 'likes_count',
                  'created_at', 'tags', 'place', 'images', 'coordinates']
        read_only_fields = ['user']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_coordinates(self, obj):
        return {'latitude': obj.latitude, 'longitude': obj.longitude}


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', "created_at"]
