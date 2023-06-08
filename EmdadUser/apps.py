from django.apps import AppConfig


class EmdaduserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EmdadUser'

    def ready(self):
        import EmdadUser.templatetags 
