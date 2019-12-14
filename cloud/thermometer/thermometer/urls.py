"""thermometer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from .admin import admin_site
from .routers import ROUTER

from temperature import viewsets as temp_vs
from auth_extension import viewsets as auth_vs

ROUTER.register('users', auth_vs.UserViewset)
ROUTER.register('profiles', auth_vs.UserProfileViewset)
ROUTER.register('thermometers', temp_vs.ThermometerViewset)
ROUTER.register('temperatures', temp_vs.TemperatureReadingViewset)

urlpatterns = [
    path('admin/', admin_site.urls),
    path('rest-auth/', include(('rest_auth.urls', 'rest_auth'))),
    path('', include(ROUTER.urls))
]
