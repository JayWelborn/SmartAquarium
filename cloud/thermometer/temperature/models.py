from random import randint
import uuid

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone

from .exceptions import ThermometerRegistrationError


# Create your models here.
class Thermometer(models.Model):
    """Stores information about thermometers

    Fields:
        owner: User who owns this thermometer
        uuid: Unique 16-character ID
        display_name: Name user gives to thermometer
        created_date: Date object was created
        registration_date: Date user registered thermometer

    Methods:
        register: Register a thermometer with a given ID. You must have the models ID to register.
            At the time of registration, the registration_date will be set to the current date. If
            provided the wrong date, registration should fail and raise
            ThermometerRegistrationError.

    References:
    """

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='thermometers',
        blank=True,
        null=True
    )
    therm_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    display_name = models.CharField(max_length=75, default=f'Smart Thermometer{randint(0, 10000)}')
    created_date = models.DateField(default=timezone.now)
    registered = models.BooleanField(default=False)
    registration_date = models.DateField(blank=True, null=True)

    def register(self, owner):
        """
        Register thermometer to provided user. If this thermometer is already
        registered, raise ThermometerRegistrationError.
        """
        if not self.registered:
            self.owner = owner
            self.registered = True
            self.registration_date = timezone.now()
            with transaction.atomic():
                self.save()
        else:
            raise ThermometerRegistrationError("Thermometer Already Registered")


class TemperatureReading(models.Model):
    """Class for a single temperature reading.

    Fields:
        thermometer: Thermometer related to this temperature record
        degrees_c: Degrees Celsius at time of reading. Stored as celsius for accuracy, because
            DS18B20 digital thermometers return data in Celsius by default.
        time_recorded: Datetime temperature was recorded. Stored in UTC for later conversion to
            timezone of user's choice

    Methods:
        convert_to_farenheit: Convert this temperature reading to F

    References:

    """
    
    thermometer = models.ForeignKey(
        Thermometer,
        on_delete=models.CASCADE,
        related_name='temperatures',
    )
    degrees_c = models.DecimalField(
        decimal_places=6,
        max_digits=10
    )
    time_recorded = models.DateTimeField(default=timezone.now)

    def get_fahrenheit(self):
        """
        Convert temperature to Fahrenheit 
        """
        return self.degrees_c * 1.8 + 32
