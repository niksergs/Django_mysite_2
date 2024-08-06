from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.blog.feeds import LatestPostFeed


handler403 = 'apps.blog.views.tr_handler403'    # Кастомная обработка ошибки 403
handler404 = 'apps.blog.views.tr_handler404'    # Кастомная обработка ошибки 404
handler500 = 'apps.blog.views.tr_handler500'    # Кастомная обработка ошибки 500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls')),
    path('', include('apps.accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),               # HTML-редактор
    path('feeds/latest/', LatestPostFeed(), name='latest_post_feed'),   # RSS лента
]

if settings.DEBUG:
    # Для работы media в режиме DEBUG = True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Включение Django Debug Toolbar
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
