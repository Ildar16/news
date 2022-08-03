from django.apps import AppConfig


class News11Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news11'

    def ready(self):
        import news11.signals
