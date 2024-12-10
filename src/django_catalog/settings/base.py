import logging
import os
from os import path
from pathlib import Path

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_catalog.settings.env_config import env_config

logger = logging.getLogger()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_config.SECRET_DJANGO
# SECURITY WARNING: don't run with debug turned on in production!

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Application definition

SITE_ID = 1

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "phonenumber_field",
    "dal",
    "dal_select2",
    "smart_selects",
    "apps.main",
    "apps.orders",
    "django_cleanup",
    "easy_thumbnails",
    "drf_spectacular",
    "silk",
    "debug_toolbar",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "django_catalog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_catalog.wsgi.application"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTERS_BACKEND": ("django_filters.rest_framework.DjangoFiltersBackend",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Mebel Tut",
    "DESCRIPTION": "API приложения компании Mebel Tut",
    "VERSION": "0.2.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env_config.POSTGRES_DB,
        "USER": env_config.POSTGRES_USER,
        "PASSWORD": env_config.POSTGRES_PASSWORD,
        "HOST": env_config.POSTGRES_HOST,
        "PORT": env_config.POSTGRES_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


LANGUAGE_CODE = "ru-Ru"

TIME_ZONE = "Europe/Minsk"

USE_I18N = True

USE_TZ = True

DATE_INPUT_FORMATS = [
    "%d.%m.%Y",  # Custom input
    "%Y-%m-%d",  # '2006-10-25'
    "%m/%d/%Y",  # '10/25/2006'
    "%m/%d/%y",  # '10/25/06'
    "%b %d %Y",  # 'Oct 25 2006'
    "%b %d, %Y",  # 'Oct 25, 2006'
    "%d %b %Y",  # '25 Oct 2006'
    "%d %b, %Y",  # '25 Oct, 2006'
    "%B %d %Y",  # 'October 25 2006'
    "%B %d, %Y",  # 'October 25, 2006'
    "%d %B %Y",  # '25 October 2006'
    "%d %B, %Y",  # '25 October, 2006'
]

DATETIME_INPUT_FORMATS = [
    "%d.%m.%Y %H:%M:%S",  # Custom input
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


INTERNAL_IPS = [
    "127.0.0.1",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "django_cache"),
    },
    "redis": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    },
}

CACHE_TIMEOUTS = {
    "5_seconds": 5,
    "5_minutes": 5 * 60,  # 5 минут (в секундах)
    "10_minutes": 10 * 60,  # 10 минут (в секундах)
    "1_hour": 60 * 60,  # 1 час (в секундах)
    "6_hours": 6 * 60 * 60,  # 6 часов (в секундах)
    "12_hours": 12 * 60 * 60,  # 12 часов (в секундах)
    "1_day": 24 * 60 * 60,  # 1 день (в секундах)
}

THUMBNAIL_ALIASES = {
    "": {
        "avatar": {"size": (500, 500), "crop": True},
    },
}

UNFOLD = {
    "SITE_TITLE": "Mebel Tut",
    "SITE_HEADER": "Mebel Tut",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("main/img/logo.png"),
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "django_catalog.settings.environment_callback",
    "DASHBOARD_CALLBACK": "apps.main.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("main/img/logo.png"),
    },
    "COLORS": {
        "primary": {
            "50": "#fbeae5",
            "100": "#f7d1c8",
            "200": "#f2a891",
            "300": "#ed8464",
            "400": "#e96b48",
            "500": "#e55e31",
            "600": "#d4552c",
            "700": "#b84726",
            "800": "#963a20",
            "900": "#7a301b",
            "950": "#43180e",
        }
    },
    "TABS": [
        {
            "models": ["main.product"],
            "items": [
                {
                    "title": _("Товары"),
                    "link": reverse_lazy("admin:main_product_changelist"),
                },
                {
                    "title": _("На акции"),
                    "link": lambda request: f"{reverse_lazy('admin:main_product_changelist')}?isOnSale__exact=True",
                },
                {
                    "title": _("Рейтинговые"),
                    "link": lambda request: f"{reverse_lazy('admin:main_product_changelist')}?rating__gt=850",
                },
            ],
        },
        {
            "models": ["orders.order"],
            "items": [
                {
                    "title": _("Все"),
                    "link": lambda request: f"{reverse_lazy('admin:orders_order_changelist')}",
                },
                {
                    "title": _("Новые"),
                    "link": lambda request: f"{reverse_lazy('admin:orders_order_changelist')}?status__exact=New",
                },
                {
                    "title": _("Текущие"),
                    "link": lambda request: f"{reverse_lazy('admin:orders_order_changelist')}?status__exact=In+progress",
                },
                {
                    "title": _("Завершённые"),
                    "link": lambda request: f"{reverse_lazy('admin:orders_order_changelist')}?status__exact=Completed",
                },
                {
                    "title": _("Отменённые"),
                    "link": lambda request: f"{reverse_lazy('admin:orders_order_changelist')}?status__exact=Cancelled",
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Навигация"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Cтатистика"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "goodtoeat_badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Товары"),
                        "icon": "bed",
                        "link": reverse_lazy("admin:main_product_changelist"),
                    },
                    {
                        "title": _("Заявки"),
                        "icon": "feedback",
                        "link": reverse_lazy("admin:main_feedback_changelist"),
                    },
                    {
                        "title": _("Заказы"),
                        "icon": "Orders",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": _("Доставка"),
                        "icon": "map",
                        "link": reverse_lazy("admin:orders_delivery_changelist"),
                    },
                ],
            },
        ],
    },
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
