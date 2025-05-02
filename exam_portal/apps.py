from django.apps import AppConfig


class ExamPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exam_portal'

    def ready(self):
        # Import signals when the app is ready
        import exam_portal.signals
