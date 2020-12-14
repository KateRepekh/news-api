from celery import shared_task

from board.models import Upvote


@shared_task
def reset_upvotes():
    Upvote.objects.all().delete()
