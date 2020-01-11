from rest_framework import viewsets, mixins

from utils.permissions import IsOwnerOrStaff, IsSelfOrAdmin, IsUserOrReadOnly

from .models import Thermometer, TemperatureReading
from .permissions import IsThermometerOwnerOrStaff
from .serializers import ThermometerSerializer, TemperatureReadingSerializer


class ThermometerViewset(viewsets.ModelViewSet):
    """Viewset for Thermometers

    Fields:
        serializer_class: Serializer used to convert thermometer to JSON
        permission_classes: restrictions on who can access which http methods

    Methods:
        get_queryset: Return all records if user is staff, otherwise the records associated with the
            current user
        create: Create a new thermometer record and register it to the currently authenticated user
    """
    serializer_class = ThermometerSerializer
    permission_classes = (IsOwnerOrStaff,)

    def get_queryset(self):
        """
        If current user is staff, return all thermometers. Otherwise return the thermometers owned
        ther current user.
        """
        if self.request.user.is_staff:
            return Thermometer.objects.all()
        return Thermometer.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new thermometer record registered to the authenticated user
        """
        thermometer = serializer.save()
        thermometer.register(self.request.user)


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
