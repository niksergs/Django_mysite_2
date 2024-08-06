from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных окружения из .env.local
def load_env_file(filepath):
    with open(filepath) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


load_env_file('.env.local')


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = bool(int(os.environ.get('DEBUG')))

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    '127.0.0.1',    # Добавляем данный параметр для локальной работы Django Debug Toolbar
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',                             # Приложение для создания древовидной модели в админке
    'django_mptt_admin',                # Приложение для улучшения визуального вида древовидной модели в админке
    'debug_toolbar',                    # Приложение Django Debug Toolbar для отладки SQL запросов
    'taggit',                           # Приложение для реализации функции тегов
    'django_recaptcha',                 # Приложение reCAPTCHA для защиты от спам ботов
    'ckeditor_uploader',                # HTML-редактор, который встраивается в веб-страницы
    'ckeditor',                         # HTML-редактор, который встраивается в веб-страницы

    'apps.blog.apps.BlogConfig',            # Основное приложение Блог
    'apps.accounts.apps.AccountsConfig',    # Приложение для регистрации
                                            # Приложение Блог API
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Приложение Django Debug Toolbar для отладки SQL запросов
    'apps.accounts.middleware.ActiveUserMiddleware',    # Middleware для отображения статуса пользователей
]

# Файловая система кэширования (для отображения статуса пользователей)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': (BASE_DIR / 'cache'),
    }
}

ROOT_URLCONF = 'blog_cbv.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_cbv.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = (BASE_DIR / 'static')
STATICFILES_DIRS = [BASE_DIR / 'templates/js/']

MEDIA_URL = '/media/'
MEDIA_ROOT = (BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google reCAPTCHA
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# Конфигурация HTML-редактора
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'full',
        'height': 300,
    },
}
