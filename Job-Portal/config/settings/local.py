from .base import *  # noqa: F403,F401

DEBUG = True

if 'debug_toolbar' not in INSTALLED_APPS:  # noqa: F405
    INSTALLED_APPS += ['debug_toolbar']  # noqa: F405

if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:  # noqa: F405
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa: F405

# Use local storage for development
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

