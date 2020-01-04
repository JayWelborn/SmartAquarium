from rest_framework import viewsets, mixins

from utils.permissions import IsOwnerOrStaff, IsSelfOrAdmin, IsUserOrReadOnly

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
    queryset = Thermometer.objects.all()
    serializer_class = ThermometerSerializer
    permission_classes = (IsOwnerOrStaff,)


class TemperatureReadingViewset(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """Viewset for Temperature Readings

    Fields:
        serializer_class: Serializer used to convert temperature readings to JSON
        permission_classes: Permission classes to be applied ot incoming requests

    Methods:
        get_queryset: Queryset for the view should include records owned by 
    """
    serializer_class = TemperatureReadingSerializer
    permission_classes = (IsThermometerOwnerOrStaff,)

    def get_queryset(self):
        """
        Queryset should include only thermometers related to current user. If user is staff,
        they can see all records
        """
        if self.request.user.is_staff:
            return TemperatureReading.objects.all()
        return TemperatureReading.objects.filter(thermometer__owner=self.request.user)
