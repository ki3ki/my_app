"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from userapp.views import index_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token generation
    path('api/auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh
    path('', index_view, name='landing-page'),
    path('userapp/', include('userapp.urls')),
    path('adminapp/', include('adminapp.urls')),
    path('api/auth/', include('djoser.urls')),  # Djoser endpoints for authentication
    path('api/auth/', include('djoser.urls.authtoken')),  # Djoser token endpoints
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


