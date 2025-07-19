from pathlib import Path
from dotenv import load_dotenv 
import os 


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET")
DEBUG = os.getenv("DEBUG", "False") == "True"
# DB Postgre mi SQLite mi?
DB_DEBUG = os.getenv("DB_DEBUG", "False") == "True"
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
if DEBUG:
	print("x" * 30)
	print(f"{DB_DEBUG = }")
	print("x" * 30)


ALLOWED_HOSTS = [
	'127.0.0.1',
    'pms.oneeyesystems.com',
	'www.pms.oneeyesystems.com',
    'testserver',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth
    
    # Django-allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Image cropping
    'easy_thumbnails',  # Required by django-image-cropping
    'image_cropping',   # NEW: Image cropping functionality
    
    # Local apps
    'intern_portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Required for django-allauth
]

ROOT_URLCONF = 'pms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DB_DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
if DB_DEBUG == False and (DB_NAME and DB_USER and DB_PASSWORD):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': 'localhost',
            # 'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static_files",
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site URL configuration for production
SITE_URL = os.getenv("SITE_URL", None)  # Production'da environment variable olarak set edilecek

# ================================
# DJANGO-ALLAUTH CONFIGURATION
# ================================

# Custom function to restrict login to @oneeyespace.com domain
def custom_google_account_adapter(request, sociallogin):
    """
    Custom adapter to restrict Google SSO to @oneeyespace.com domain only
    """
    user = sociallogin.user
    email = user.email
    
    if not email or not email.endswith('@oneeyespace.com'):
        from django.contrib import messages
        messages.error(request, 'Yalnızca @oneeyespace.com e-posta adresine sahip kullanıcılar giriş yapabilir.')
        return False
    
    return True

# Required for django-allauth
SITE_ID = 1

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Login/logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/portal/availability/'
LOGOUT_REDIRECT_URL = '/'

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

# Social account providers configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'FETCH_USERINFO': True,
    }
}

# Critical settings for direct OAuth flow
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True  # ← This MUST be True for direct redirect!

# Domain restriction for Google SSO
SOCIALACCOUNT_ADAPTER = 'intern_portal.adapters.CustomSocialAccountAdapter'

# Image cropping settings
from django.conf import settings as django_settings

THUMBNAIL_PROCESSORS = [
    'image_cropping.thumbnail_processors.crop_corners',
] + getattr(django_settings, 'THUMBNAIL_PROCESSORS', [])

# Easy thumbnails settings for image cropping
EASY_THUMBNAILS_ALIAS_PREFIX = 'cropped_'

# Thumbnail configurations
THUMBNAIL_ALIASES = {
    '': {
        'profile_large': {'size': (350, 350), 'crop': True, 'quality': 95},
        'profile_medium': {'size': (150, 150), 'crop': True, 'quality': 95},
        'profile_small': {'size': (60, 60), 'crop': True, 'quality': 95},
        'profile_admin': {'size': (40, 40), 'crop': True, 'quality': 95},
    },
}