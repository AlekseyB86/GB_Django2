
from django.core.management.base import BaseCommand
from authapp.models import User, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(userprofile__isnull=True)
        for user in users:
            UserProfile.objects.create(user=user)
