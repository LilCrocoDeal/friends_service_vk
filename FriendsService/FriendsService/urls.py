from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as swagger_url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('main.urls')),
    path('api/v1/auth', include('djoser.urls')),
    path('api/v1/auth', include('djoser.urls.authtoken')),
]

urlpatterns += swagger_url
