from rest_framework import permissions

from .models import TemperatureReading, Thermometer


class IsThermometerOwnerOrStaff(permissions.BasePermission):
    """
    Only expose thermometers to their owners
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, TemperatureReading):
            raise TypeError("This permission class is only for use with temperature readings")

        return obj.thermometer.owner == request.user or request.user.is_staff
