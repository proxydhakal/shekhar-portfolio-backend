"""
Local development settings.
Used when ENVIRONMENT=local (default).
"""
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
_extra_hosts = os.getenv('ALLOWED_HOSTS', '')
if _extra_hosts:
    ALLOWED_HOSTS += [h.strip() for h in _extra_hosts.split(',') if h.strip()]

# SQLite for local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Console email backend (no SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM = os.getenv('EMAIL_FROM') or os.getenv('DEFAULT_FROM_EMAIL', 'noreply@localhost')
DEFAULT_FROM_EMAIL = EMAIL_FROM

# Optional: do not use WhiteNoise manifest in local (faster)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
