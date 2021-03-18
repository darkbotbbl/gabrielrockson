from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')k_29r3w&x@@@e#mhal34r0g8^cw!3g-&y^qsq*94m)*^!z43)'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

INSTALLED_APPS += [
    
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gabrielrockson',
        'USER': 'gabriel_rockson',
        'PASSWORD': 'rockson_gabriel',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
