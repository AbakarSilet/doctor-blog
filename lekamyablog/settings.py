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
if os.getenv('ENVIRONMENT') == 'development':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost","doctorlekamyangambi.up.railway.app"]
CSRF_TRUSTED_ORIGINS = ["https://doctorlekamyangambi.up.railway.app"]

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
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2  # 2 semaines
# Durée de session prolongée pour "Se souvenir de moi"
ACCOUNT_SESSION_REMEMBER = True

handler404 = 'blog.views.custom_404' 
handler403 = 'blog.views.custom_403'

DEFAULT_CHARSET = 'utf-8'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

if DATABASE_URL:
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
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
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

# Paramètres sécurité pour la production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
# Configuration AWS/Cloudflare R2
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.r2.cloudflarestorage.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False 

# Configuration des médias
if os.getenv('ENVIRONMENT') == 'production':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if os.getenv('ENVIRONMENT') == 'production':
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # Option alternative: STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

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

