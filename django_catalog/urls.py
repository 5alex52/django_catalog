from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import CategorySitemap, CollectionSitemap, ProductSitemap
from django.views.generic.base import TemplateView
from main.views import robots_txt

handler404 = 'main.views.tr_handler404'
handler505 = 'main.views.tr_handler505'

sitemaps = {
    'category': CategorySitemap,
    'collection': CollectionSitemap,
    'product': ProductSitemap,
}

admin.site.site_header = 'Мебель тут'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", robots_txt),
    path('', include('main.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
