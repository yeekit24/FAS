from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = "src.authentication"
    verbose_name = "Authentication"

    def ready(self):
        import src.authentication.signals  # noqa F401
