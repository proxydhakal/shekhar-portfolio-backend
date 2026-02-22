"""
Production settings.
Used when ENVIRONMENT=production.
Requires .env with DB_*, EMAIL_*, ALLOWED_HOSTS set.
Static/media can be overridden for cPanel (e.g. public_html/staticfiles, public_html/media).
"""
import os
from pathlib import Path
from .base import *  # noqa: F401, F403

DEBUG = False

# ALLOWED_HOSTS must be set in .env (comma-separated)
_allowed = os.getenv('ALLOWED_HOSTS', '').strip()
if not _allowed:
    raise ValueError('Production requires ALLOWED_HOSTS in .env (comma-separated)')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

# MySQL from env (required in production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
if not DATABASES['default']['NAME'] or not DATABASES['default']['USER']:
    raise ValueError('Production requires DB_NAME, DB_USER, DB_PASSWORD (and optionally DB_HOST, DB_PORT) in .env')

# SMTP email from env (supports SSL on port 465 or TLS on 587)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').strip().lower() in ('true', '1', 'yes')
EMAIL_USE_TLS = not EMAIL_USE_SSL and os.getenv('EMAIL_USE_TLS', 'True').strip().lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM') or os.getenv('DEFAULT_FROM_EMAIL') or EMAIL_HOST_USER or 'noreply@localhost'
DEFAULT_FROM_EMAIL = EMAIL_FROM

# Static and media: allow env override; default to cPanel public_html paths when not set
_default_static_root = os.getenv('STATIC_ROOT', '/home/shekhard/public_html/staticfiles')
_default_media_root = os.getenv('MEDIA_ROOT', '/home/shekhard/public_html/media')
STATIC_ROOT = Path(_default_static_root)
MEDIA_ROOT = Path(_default_media_root)
STATIC_URL = os.getenv('STATIC_URL', '/static/')
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')

# WhiteNoise for compressed static files; override with STATICFILES_STORAGE in .env if cPanel serves static
STATICFILES_STORAGE = os.getenv(
    'STATICFILES_STORAGE',
    'whitenoise.storage.CompressedManifestStaticFilesStorage',
)

# ---------- Security (XSS, HTTPS, cookies, headers) ----------
# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# XSS and content-type protection (browser behavior)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTPS only for 1 year; enable only if you consistently serve HTTPS)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Referrer policy (no referrer for cross-origin)
SECURE_REFERRER_POLICY = 'same-origin'
