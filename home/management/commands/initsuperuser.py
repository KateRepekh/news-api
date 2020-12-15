from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            User.objects.create_superuser(
                os.environ.get("ADMIN_USERNAME", "admin"),
                os.environ.get("ADMIN_EMAIL", ""),
                os.environ.get("ADMIN_PASSWORD", "admin"),
            )
