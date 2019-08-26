from django.apps import AppConfig


class MainPageConfig(AppConfig):
    name = 'main_page'

    def ready(self):
        from .signals import populate_models
        from django.db.models.signals import post_migrate
        post_migrate.connect(populate_models, sender=self)