from rest_framework import permissions


class IsThermometerOwnerOrStaff(permissions.BasePermission):
    """
    Only expose thermometers to their owners
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, TemperatureReading):
            raise TypeError("This permission class is only for use with temperature readings")

        print("method called")

        return obj.thermometer.owner == request.user or request.user.is_staff
