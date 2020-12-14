from django.core.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from board.models import Post, Comment, Upvote
from board.serializers import PostSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user


class OwnedModelViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class PostViewSet(OwnedModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @action(detail=True, methods=['POST'],
            permission_classes=[permissions.IsAuthenticated])
    def upvote(self, request, pk=None):
        post = self.get_object()
        upvote = Upvote(post=post, owner=self.request.user)
        try:
            upvote.validate_unique()
            upvote.save()
        except ValidationError:
            Upvote.objects.filter(post=post, owner=self.request.user).delete()
        return self.retrieve(self, request, pk=pk)

    def get_serializer_class(self):
        if self.action == 'upvote':
            return Serializer
        else:
            return super().get_serializer_class()


class CommentViewSet(OwnedModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
