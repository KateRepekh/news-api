from django.db import models
from django.conf import settings


class OwnedByUserCreatedAtModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(OwnedByUserCreatedAtModel):
    title = models.CharField(max_length=128)
    link = models.URLField()
    comments = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Comment', related_name='comments'
    )
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Upvote', related_name='upvotes'
    )

    def __str__(self):
        return self.title


class OwnedByUserAndPostCreatedAtModel(OwnedByUserCreatedAtModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(OwnedByUserAndPostCreatedAtModel):
    content = models.TextField()

    def __str__(self):
        return self.content


class Upvote(OwnedByUserAndPostCreatedAtModel):
    class Meta:
        unique_together = ('post', 'owner')

    def __str__(self):
        return '{post} upvoted by {user}'.format(post=self.post,
                                                 user=self.owner)
