from django.urls import path, include

from thermometer.routers import ROUTER

from .viewsets import ThermometerViewset, TemperatureReadingViewset


router = ROUTER
router.register('thermometers', ThermometerViewset)
router.register('temperature-readings', TemperatureReadingViewset)

urlpatterns = [
     path('', include(router.urls))
]
