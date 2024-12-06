from apps.main.sitemaps import CategorySitemap
from apps.main.sitemaps import CollectionSitemap
from apps.main.sitemaps import ProductSitemap
from apps.main.views import robots_txt
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

handler404 = "apps.main.views.tr_handler404"
handler505 = "apps.main.views.tr_handler505"

sitemaps = {
    "category": CategorySitemap,
    "collection": CollectionSitemap,
    "product": ProductSitemap,
}

admin.site.site_header = "Мебель тут"


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", robots_txt),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("apps.api.urls")),
    path("", include("apps.main.urls")),
    path("orders/", include("apps.orders.urls")),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
