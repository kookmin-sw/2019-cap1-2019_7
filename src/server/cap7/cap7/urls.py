from django.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('player.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
