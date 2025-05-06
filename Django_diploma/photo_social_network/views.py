from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Django_diploma.serializers import PostSerializer, CommentSerializer, PostImageSerializer
from photo_social_network.models import Post, Comment, Like, PostImage

from Django_diploma.permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        user = request.user

        if Like.objects.filter(post=post, user=user).exists():
            Like.objects.filter(post=post, user=user).delete()
            return Response({"message": "Лайк удален"})
        else:
            Like.objects.create(post=post, user=user)
            return Response({"message": "Лайк поставлен"})


class PostImageViewSet(ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request):
        post_id = request.data['post']
        image = request.FILES['image']
        post_image = PostImage.objects.create(post_id=post_id, image=image)
        return Response(PostImageSerializer(post_image).data)
