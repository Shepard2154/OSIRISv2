from django.apps import AppConfig


class SpecialConfig(AppConfig):
    name = 'special'

    def ready(self):
        import celery