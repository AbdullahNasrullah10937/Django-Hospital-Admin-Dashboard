"""
Django settings for BP_Hospitals project.

Configured for BP Hospitals - Admin Management System.
All key configuration blocks contain explicit comments for evaluation.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-nv756d=ibeqdue@2xu0efp3vtz_yx9&#_3uc#$85#b^7cd2_*2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# ==============================================================================
# CSRF & COOKIE SECURITY CONFIGURATION
# ==============================================================================
# Django 4.0+ requires CSRF_TRUSTED_ORIGINS for any HTTPS deployment.
# Without this, all POST forms (login, create, update, delete) return 403 Forbidden.
# Covers both Vercel preview URLs and the primary production domain.
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://django-hospital-admin-dashboard.vercel.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Secure cookies on HTTPS (Vercel always uses HTTPS)
if os.environ.get('VERCEL'):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SAMESITE = 'Lax'


# ==============================================================================
# 1. INSTALLED APPS CONFIGURATION
# ==============================================================================
# Register Django built-in core applications alongside the three custom domain-specific
# applications created for BP Hospitals: 'hospitals', 'directors', and 'wards'.
INSTALLED_APPS = [
    # Django Built-in Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # BP Hospitals Custom Domain Apps
    'hospitals.apps.HospitalsConfig',
    'directors.apps.DirectorsConfig',
    'wards.apps.WardsConfig',
]


# ==============================================================================
# MIDDLEWARE CONFIGURATION
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add WhiteNoise for serving static files in production when available
try:
    import whitenoise
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ImportError:
    pass



# ==============================================================================
# 2. ROOT URL CONFIGURATION
# ==============================================================================
# Points explicitly to the project's root URL configuration file (BP_Hospitals/urls.py),
# which routes requests to admin, authentication, and individual app URL files.
ROOT_URLCONF = 'BP_Hospitals.urls'


# ==============================================================================
# 3. TEMPLATES CONFIGURATION
# ==============================================================================
# Enables Django Template Language (DTL).
# - DIRS: Points to the root 'templates' directory for global layouts (base.html, dashboard.html, login.html).
# - APP_DIRS: True allows Django to look inside each app's 'templates' folder (e.g. hospitals/templates/).
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'BP_Hospitals.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'BP_Hospitals.wsgi.application'


# ==============================================================================
# 4. DATABASES CONFIGURATION
# ==============================================================================
# Configured dynamically: uses DATABASE_URL if available (e.g., Render PostgreSQL),
# falling back to SQLite for local development.
# 
# NOTE ON SWAPPING TO MYSQL FOR PRODUCTION:
# To use MySQL instead of SQLite, install 'mysqlclient' or 'PyMySQL' and update DATABASES as follows:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bp_hospitals_db',
#         'USER': 'bp_admin',
#         'PASSWORD': 'secure_password_here',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }
import shutil

# Vercel Serverless Writable Database Handler
IS_VERCEL = 'VERCEL' in os.environ

if IS_VERCEL:
    tmp_db_path = '/tmp/db.sqlite3'
    orig_db_path = BASE_DIR / 'db.sqlite3'
    if not os.path.exists(tmp_db_path) and os.path.exists(orig_db_path):
        shutil.copyfile(orig_db_path, tmp_db_path)
    db_location = tmp_db_path
else:
    db_location = str(BASE_DIR / 'db.sqlite3')

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{db_location}',
        conn_max_age=600
    )
}




# ==============================================================================
# PASSWORDS & AUTHENTICATION CONFIGURATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Authentication Redirect URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'


# ==============================================================================
# INTERNATIONALIZATION CONFIGURATION
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 5. STATIC FILES CONFIGURATION
# ==============================================================================
# STATIC_URL defines the base URL for referencing static files (CSS, JS, Images).
# STATICFILES_DIRS specifies additional filesystem directories to search for static assets.
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
