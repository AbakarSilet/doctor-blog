import os
from pathlib import Path
from dotenv import load_dotenv

from urllib.parse import urlparse
import dj_database_url


# Charger les variables d'environnement
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [
    'docteurbenido.up.railway.app',
    '127.0.0.1',
    'localhost'
]

# Configuration pour Railway
CSRF_TRUSTED_ORIGINS = [
    'https://docteurbenido.up.railway.app',
    'https://*.railway.app'
]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'blog',
    'accounts',
    
    "anymail",
    "storages",
]

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
# Durée de session par défaut
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2  # 2 semaines
# # Durée de session prolongée pour "Se souvenir de moi"
# ACCOUNT_SESSION_REMEMBER = True

handler404 = 'blog.views.custom_404' 
handler403 = 'blog.views.custom_403'

DEFAULT_CHARSET = 'utf-8'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lekamyablog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'lekamyablog.wsgi.application'



DATABASE_URL = os.environ.get('DATABASE_URL')

if os.getenv('ENVIRONMENT') == 'production':
    db_info = urlparse(DATABASE_URL)
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_info.path[1:],  
            'USER': db_info.username,
            'PASSWORD': db_info.password,
            'HOST': db_info.hostname,
            'PORT': db_info.port,
            'OPTIONS': {
                'sslmode': 'require',  
            },
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME': os.getenv('LOCAL_DATABASE_NAME'),
        'USER': os.getenv('LOCAL_DATABASE_USER'),
        'PASSWORD': os.getenv('LOCAL_DATABASE_PASSWORD'),
        'HOST': os.getenv('LOCAL_DATABASE_HOST'),
        'PORT': os.getenv('LOCAL_DATABASE_PORT'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Configuration du stockage par défaut pour les médias
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    
    # Configuration AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_SIGNATURE_NAME = 's3v4'
    AWS_S3_REGION_NAME = 'eu-north-1'
    AWS_S3_VERIFY = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    
    # Définition de MEDIA_URL pour qu'il pointe vers S3
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'


TIME_ZONE = 'Africa/Ndjamena'

USE_TZ = True
USE_I18N = True 
USE_L10N = True 


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
DEFAULT_FROM_EMAIL = "benidongambilekamya@gmail.com"

ANYMAIL = {
    "BREVO_API_KEY": os.getenv('BREVO_API_KEY'),
    "IGNORE_UNSUPPORTED_FEATURES": True,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Dr Lekamya Ngambi BenIdo",
    "site_header": "Administration du site",
    "site_logo": "assets/img/favicon.png",
    "theme": "slate",
    "navigation_expanded": True,
    "copyright": "Abakarix4dev",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        # Icônes pour l'app "blog"
        "blog.Article": "fas fa-book",
        "blog.Commentaire": "fas fa-comment",
        "blog.Reponse": "fas fa-reply",
        
        "accounts.User": "fas fa-user",
    },
    "custom_links": {
        "books": [{
            "name": "Voir le site public",
            "url": "https://monsite.com",
            "icon": "fas fa-globe",
            "permissions": ["auth.view_user"]
        }]
    },
    "custom_css": "admin/css/custom_admin.css",
}

