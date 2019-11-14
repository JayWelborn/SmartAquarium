from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


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

    References:
    """

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='thermometers')
    uuid = models.UUIDField(unique=True, editable=False)
    display_name = models.CharField(max_length=75, default='Thermometer Name Not Provided')
    created_date = models.DateField(default=datetime.utcnow)
    registration_date = models.DateField()
