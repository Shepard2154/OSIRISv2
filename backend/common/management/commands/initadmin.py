from asyncio.log import logger
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            User.objects.create_superuser('admin', 'admin@myproject.com', 'password')
        except IntegrityError:
            pass