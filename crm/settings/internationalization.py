import os
from .base import BASE_DIR
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Farsi')),
]
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Tehran'
USE_TZ = True
USE_I18N = True
USE_L10N = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]
