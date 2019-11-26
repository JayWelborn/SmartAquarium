from datetime import datetime
from random import randint
import uuid

from django.db import models
from django.contrib.auth import get_user_model

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
        provided the wrong date, registration should fail and raise ThermometerRegistrationError.

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
    created_date = models.DateField(default=datetime.utcnow)
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
            self.registration_date = datetime.utcnow()
            self.save()
        else:
            raise ThermometerRegistrationError("Thermometer Already Registered")

