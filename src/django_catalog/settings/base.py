import logging
import os
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
    "apps.main",
    "apps.api",
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
        "DIRS": [],
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
    }
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
    "SITE_ICON": lambda request: static(
        "main/img/logo.png"
    ),  # both modes, optimise for 32px height
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "ENVIRONMENT": "django_catalog.settings.environment_callback",
    # "DASHBOARD_CALLBACK": "dashboard_callback",
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
    ],
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "goodtoeat_badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Пользователи"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Товары"),
                        "icon": "Grocery",
                        "link": reverse_lazy("admin:main_product_changelist"),
                    },
                    # {
                    #     "title": _("Заказы"),
                    #     "icon": "Grocery",
                    #     "link": reverse_lazy("admin:products_product_changelist"),
                    # },
                ],
            },
        ],
    },
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
