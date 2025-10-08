import os
from pathlib import Path

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY"))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["mebeltut24.by", "127.0.0.1"]

MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID")
TECH_CHANNEL_ID = os.getenv("TECH_CHANNEL_ID")
TECH_BOT_TOKEN = os.getenv("TECH_BOT_TOKEN")


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = "/home/yuma/public_html/media"
#MEDIA_ROOT = "media"


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
    "main",
    "django_cleanup",
    "easy_thumbnails",
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yuma_db',
        'USER': 'yuma_user',
        'PASSWORD': 'django_user031203',
        'HOST': 'localhost',
        'PORT': '',
    }
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
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

DEFAULT_CHARSET = "utf-8"


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

UNFOLD = {
    "SITE_TITLE": "Mebel Tut",
    "SITE_HEADER": "Mebel Tut",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("main/img/logo.png"),
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "DASHBOARD_CALLBACK": "main.views.dashboard_callback",
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
                    "link": lambda request: f"{reverse_lazy('admin:main_product_changelist')}?isOnSale__exact=1",
                },
                {
                    "title": _("Рейтинговые"),
                    "link": lambda request: f"{reverse_lazy('admin:main_product_changelist')}?rating_from=850",
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
                        "title": _("Главная"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
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
                ],
            },
        ],
    },
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
