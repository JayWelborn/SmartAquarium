from rest_framework import serializers

from .models import Thermometer, TemperatureReading

class TemperatureReadingSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Temperature readings to JSON

    Fields:
        thermometer: Thermometer associated with this temperature reading
    
    Metaclass Fields:
        model: Model to be serialized
        fields: Fields included in serialization
        read_only_fields: Specifies these fields as read only

    """
    thermometer = serializers.ReadOnlyField(source='thermometer.display_name')

    class Meta:
        model = TemperatureReading
        fields = ('url', 'id', 'thermometer', 'degrees_c', 'time_recorded')
        read_only_fields = ('thermometer', 'time_recorded')

    def update(self, instance, validated_data):
        """
        Overwrite to disallow updating temp records through serializer
        """
        msg = "Updating Temperature Readings via API not allowed. " + \
              "Contact a system administrator for assistance."
        raise TypeError(msg)


class ThermometerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Thermometers to JSON.

    Fields:
        temperatures: Temperature readings associated with this thermometer
        owner: User who owns this thermometer
    
    Metaclass Fields:
        model: Model to be serialized
        fields: Fields to include in serialization
        read_only_fields: Specifies fields as read only

    """
    temperatures = TemperatureReadingSerializer(
        many=True, read_only=False)
    owner = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = Thermometer
        fields = ('url', 'owner', 'temperatures', 'therm_id', 'display_name', 'created_date', 'registered', 'registration_date')
        read_only_fields = ('therm_id', 'owner', 'created_date', 'registration_date', 'registered')
