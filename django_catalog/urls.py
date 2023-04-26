from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'main.views.tr_handler404'
handler505 = 'main.views.tr_handler505'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)