from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from posts.views import (index, blog, post, search, create_post, update_post, delete_post)
from filebrowser.sites import site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('blog/', blog, name='blog'),
    path('post/<id>/', post, name='post'),
    path('search/', search, name='search'),
    path('post/create', create_post, name='create_post'),
    path('post/<id>/update', update_post, name='update_post'),
    path('post/<id>/delte', delete_post, name='post_delete'),
    path('tinymce/', include('tinymce.urls')),
    re_path(r'^admin/filebrowser/', site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
