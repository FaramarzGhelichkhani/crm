from dotenv import load_dotenv
from crm.settings import BASE_DIR
import os

load_dotenv()

DEBUG = os.getenv('DEBUG', 'True')
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS_ = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = ALLOWED_HOSTS_ + ['localhost', '192.168.1.137']

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 315360000  # 10 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"

    ALLOWED_HOSTS = ALLOWED_HOSTS_
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
