from rest_framework import serializers
from timezone_field import TimeZoneField as TimeZoneField_


class TimeZoneField(serializers.ChoiceField):
    """
    Wrapper for 3rd party Time Zone Field
    """
    def __init__(self, **kwargs):
        super().__init__(TimeZoneField_.CHOICES + [(None, "")], **kwargs)

    def to_representation(self, value):
        return str(super().to_representation(value))
