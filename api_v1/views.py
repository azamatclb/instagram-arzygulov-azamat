from webapp.models.post import Post
from .serializers.post import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from api_v1.permission import IsOwnerOrReadOnly


# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'like', 'unlike']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            post.likes_count += 1
            post.save()
        return Response({'status': 'liked'})

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.likes_count -= 1
            post.save()
        return Response({'status': 'unliked'})
