from .base import *

DEBUG = True

if 'debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS += ['debug_toolbar']

if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

