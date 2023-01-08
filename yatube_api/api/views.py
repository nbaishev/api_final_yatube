from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter

from api.serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                             PostSerializer)
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnlyPermission
from posts.models import Follow, Group, Post, User


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого поста запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого поста запрещено!')
        return super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id).comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого коммента запрещено!')
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого коммента запрещено!')
        return super(CommentViewSet, self).perform_destroy(instance)

class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Group."""

    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username', 'user__username',)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Follow.objects.filter(user=self.request.user)
        raise NotAuthenticated('xwhat')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
