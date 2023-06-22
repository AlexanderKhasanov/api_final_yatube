from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ValidationError
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from .permissions import IsAuthorOrReadOnly
from .custom_viewset import ListCreateViewSet
from .serializers import (PostSerializer, CommentSerializer, GroupSerializer,
                          FollowSerializer)
from posts.models import Post, Comment, Group, Follow

User = get_user_model()


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(
            author=self.request.user,
            post=post,
        )


class FollowViewSet(ListCreateViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.follower.all()

    def perform_create(self, serializer):
        following_username = serializer.validated_data.get('following')
        following = get_object_or_404(User, username=following_username)
        if following == self.request.user:
            raise ValidationError('Нельзя подписаться на самого себя')
        follow = Follow.objects.filter(
            user=self.request.user,
            following=following
        )
        if follow.exists():
            raise ValidationError('Вы уже подписаны на данного автора')
        serializer.save(
            user=self.request.user,
            following=following
        )
