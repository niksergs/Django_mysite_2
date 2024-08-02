from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls')),
    path('', include('apps.accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),   # HTML-редактор
]

if settings.DEBUG:
    # Для работы media в режиме DEBUG = True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Включение Django Debug Toolbar
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
