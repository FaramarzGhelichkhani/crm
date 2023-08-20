from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmdaduserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.EmdadUser'
    verbose_name = _('user')
