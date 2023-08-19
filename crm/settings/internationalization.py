from .base import BASE_DIR
from django.utils.translation import gettext_lazy as _
import os

# DEFAULT_CHARSET = 'utf-8'
LANGUAGES = [
    ('en', _('English')),  # todo add translate with _
    ('fa', _('Farsi')),
]
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]
