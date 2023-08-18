from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "rest_framework",
    'rest_framework.authtoken',

    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third party apps
    'crispy_forms',
    "crispy_tailwind",
    'tailwind',
    'theme',
    'apps.Order',
    'apps.company',
    'apps.Emdad',
    'apps.EmdadUser',
    'apps.Transaction',
    #
    'jalali_date',
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S  %y/%m/%d',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}


USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
DECIMAL_SEPARATOR = '.'
NUMBER_GROUPING = 3

ROOT_URLCONF = 'crm.urls'
WSGI_APPLICATION = 'crm.wsgi.application'
TAILWIND_APP_NAME = 'theme'
