from rest_framework import viewsets, mixins

from utils.permissions import IsOwnerOrReadOnly, IsSelfOrAdmin, IsUserOrReadOnly

from .models import Thermometer, TemperatureReading
from .permissions import IsThermometerOwnerOrStaff
from .serializers import ThermometerSerializer, TemperatureReadingSerializer


class ThermometerViewset(viewsets.ModelViewSet):
    """Viewset for Thermometers

    Fields:
        queryset: List of thermometers ordered by created date
        serializer_class: Serializer used to convert thermometer to JSON
        permission_classes: restrictions on who can access which http methods
    """
    queryset = Thermometer.objects.all().order_by('created_date')
    serializer_class = ThermometerSerializer
    permissions_classes = (IsOwnerOrReadOnly,)


class TemperatureReadingViewset(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """Viewset for Temperature Readings

    Fields:
        queryset: List of temperature readings sorted by date
        serializer_class: Serializer used to convert temperature readings to JSON
    """
    queryset = TemperatureReading.objects.all().order_by('time_recorded')
    serializer_class = TemperatureReadingSerializer
    permission_classes = (IsThermometerOwnerOrStaff,)
    