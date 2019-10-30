from django.urls import path, include

from thermometer.routers import ROUTER

from .viewsets import UserViewset, UserProfileViewset


router = ROUTER
router.register('users', UserViewset)
router.register('profiles', UserProfileViewset)

urlpatterns = [
    path('', include(router.urls))
]
