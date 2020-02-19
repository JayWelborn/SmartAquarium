from django.db import transaction

from rest_framework import serializers

from .exceptions import ThermometerCreationError
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
        read_only_fields = ('id', 'thermometer', 'time_recorded')

    def update(self, instance, validated_data):
        """
        Overwrite to disallow updating temp records through serializer
        """
        msg = 'Updating Temperature Readings via API not allowed. ' + \
              'Contact a system administrator for assistance.'
        raise TypeError(msg)


class ThermometerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Thermometers to JSON.

    Fields:
        temperatures: Temperature readings associated with this thermometer
        owner: User who owns this thermometer
        allowed_on_post: Fields that can be set via the API in new object creation
    
    Metaclass Fields:
        model: Model to be serialized
        fields: Fields to include in serialization
        read_only_fields: Specifies fields as read only

    Methods:
        create: Create new thermometer record. When thermometers are created, they should not have
            any associated temperature readings, so if temperature readings are included throw an
            error.
        update: Update an existing thermometer record.
    """
    temperatures = TemperatureReadingSerializer(
        many=True, read_only=False, required=False, allow_null=True)
    owner = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)
    allowed_on_post = set(('therm_id', 'display_name'))

    class Meta:
        model = Thermometer
        fields = ('url', 'owner', 'temperatures', 'therm_id',
                  'display_name', 'created_date', 'registered', 'registration_date')
        read_only_fields = ('owner', 'created_date', 'registration_date', 'registered')
    
    def create(self, validated_data):
        """
        Create new thermometer record. When thermometers are created, they should not have
        any associated temperature readings, so if temperature readings are included throw an
        error.
        """
        thermometer = Thermometer.objects.create()
        
        for key, value in validated_data.items():
            if key in self.allowed_on_post:
                setattr(thermometer, key, value)
        
        with transaction.atomic():
            thermometer.save()
        return thermometer

    def update(self, instance, validated_data):
        """
        Update an existing thermometer record. This is the method by which new temperature readings
        will be associated with an existing thermomter.
        """
        temps = []
        if 'temperatures' in validated_data:
            temps = validated_data['temperatures']
        
        # Update instance fields
        for key, value in validated_data.items():
            if (
                key in dir(instance) and
                validated_data[key] != getattr(instance, key) and
                key != 'temperatures'
            ):
                setattr(instance, key, value)

        for temp in temps:
            new_reading = TemperatureReading.objects.create(
                degrees_c=temp['degrees_c'],
                thermometer=instance
            )
            with transaction.atomic():
                new_reading.save()
                     
        with transaction.atomic():
            instance.save()
        return instance

    def validate_temperatures(self, value):
        if not self.instance and value:
            raise serializers.ValidationError(
                'New Thermometers cannot be created with temperature readings'
            )
        return value
