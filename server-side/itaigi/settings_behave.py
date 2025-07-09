from .settings import INSTALLED_APPS
from .settings import *  # noqa

INSTALLED_APPS += (
    'behave_django',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
