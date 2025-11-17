from pathlib import Path
from decouple import config


# BUILD PATHS INSIDE THE PROJECT LIKE THIS: BASE_DIR / 'SUBDIR'.
BASE_DIR = Path(__file__).resolve().parent.parent

# THE SECRET KEY IS PLACED IN .ENV FOLDER TO EXCLUDE IT FROM GIT
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DEBUG')

ALLOWED_HOSTS = []

# CUSTOM USER AUTHENTIFICATION MODEL
AUTH_USER_MODEL = 'accounts.CustomUser'

# CUSTOM USER AUTHENTIFICATION BACKEND
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
]

# APPLICATION DEFINITION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'play_pal.apps.PlayPalConfig',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'play_pal_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'play_pal_project.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'accounts.validators.CustomComplexityValidator', 'OPTIONS': {'min_length': 10}},
]


# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC FILES (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# DEFAULT PRIMARY KEY FIELD TYPE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
