from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.main"
    verbose_name = "Главное"

    def ready(self):
        import apps.main.signals
