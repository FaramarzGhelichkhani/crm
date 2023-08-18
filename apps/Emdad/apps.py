from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmdadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Emdad'
    verbose_name = _('Emdad')
