from rest_framework import serializers

from board.models import Post, Comment


class ExcludeListType(type):
    def __new__(cls, name, bases, attrs):
        exclude = []
        for base in bases:
            if hasattr(base, "exclude"):
                exclude.extend(base.exclude)
        attrs["exclude"] = exclude + attrs.get("exclude", [])
        return type.__new__(cls, name, bases, attrs)


class OwnedByUserModelSerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.CharField(
        source="owner.username", read_only=True
    )

    class Meta(metaclass=ExcludeListType):
        exclude = ["owner"]


class PostSerializer(OwnedByUserModelSerializer):
    upvote_count = serializers.IntegerField(
        source="upvotes.count", read_only=True
    )

    class Meta(OwnedByUserModelSerializer.Meta):
        model = Post
        exclude = ["upvotes"]
        extra_kwargs = {"comments": {"view_name": "comment-detail"}}


class CommentSerializer(OwnedByUserModelSerializer):
    class Meta(OwnedByUserModelSerializer.Meta):
        model = Comment
