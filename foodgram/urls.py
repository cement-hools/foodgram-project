from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from foodgram import settings

urlpatterns = [
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),

    path('', include('recipes.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
