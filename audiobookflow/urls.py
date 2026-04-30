"""
URL configuration for audiobookflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),  # Главная и каталог
    path('accounts/', include('accounts.urls')),  # Авторизация (Шаг 4)
    path('player/', include('player.urls')),      # Плеер/прогресс (Шаг 5)
]

# Отдача медиа-файлов (обложки, аудио) только при DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        path('protected_media/<path:path>', serve, {
            'document_root': settings.PROTECTED_MEDIA_ROOT,
        }),
    ]