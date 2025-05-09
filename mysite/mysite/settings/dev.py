import sys

from .base import *

from django.urls import include, path

from debug_toolbar.toolbar import debug_toolbar_urls


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TESTING = "test" in sys.argv

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0i#riesb1sy1x)4f&$#b*^j2bk72-b9n@u1+xh#^4hx%731@s3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if DEBUG and not TESTING:
    INSTALLED_APPS = INSTALLED_APPS + [
        "debug_toolbar",
        "django_extensions",
        "wagtail.contrib.styleguide",
    ]

    MIDDLEWARE = MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INTERNAL_IPS = [
        "127.0.0.1", # localhost
        "127.17.0.1", # docker	
    ]
    
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "C:\\Users\\kozl\\ITProjects\\WagtailCMS_web\\mysite\\cache",
        }
    }
    
try:
    from .local import *
except ImportError:
    pass
