"""
Django settings entry point.
Uses ENVIRONMENT (local | production) to load the appropriate settings module.
"""
import os

from dotenv import load_dotenv
from pathlib import Path

# Load .env before reading ENVIRONMENT
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')

ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').strip().lower()
if ENVIRONMENT not in ('local', 'production'):
    ENVIRONMENT = 'local'

if ENVIRONMENT == 'production':
    from .production import *  # noqa: F401, F403
else:
    from .local import *  # noqa: F401, F403
