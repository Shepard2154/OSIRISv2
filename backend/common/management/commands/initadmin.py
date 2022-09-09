from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import DoesNotExist


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            User.objects.get(username="admin")
            User.objects.create_superuser('admin', 'admin@myproject.com', 'password')
        except DoesNotExist:
            self.stdout.write("Admin account has already existed")