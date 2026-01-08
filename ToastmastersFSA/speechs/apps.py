from django.apps import AppConfig


class SpeechsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "speechs"
    
    def ready(self):
        import speechs.signals