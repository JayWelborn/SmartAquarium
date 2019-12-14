from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.test import APITestCase

from temperature.models import Thermometer, TemperatureReading
from temperature.serializers import TemperatureReadingSerializer


class TemperatureReadingSerializerTests(APITestCase):
    """Tests for Temperature Reading Serializer

    Methods:
        setUp: create test data
        tearDown: clear test database
        test_serializer_valid_data: when given valid data, serializer should create a new
            temperature reading record

    """

    def setUp(self):
        """
        create test data
        1 User
        1 Thermometer
        1 `context` dictionary
        """
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass",
            email="e@ma.il"
        )
        with transaction.atomic():
            self.user.save()
        
        self.thermometer = Thermometer(
            display_name='therm'
        )
        with transaction.atomic():
            self.thermometer.register(self.user)
        
        self.context = {'request': None}

    def tearDown(self):
        """
        clear test database
        """
        with transaction.atomic():
            self.user.delete()

    def test_temperature_reading_serialized_correctly(self):
        """
        Serialized readings should include all fields specified
        """
        temp = TemperatureReading(            
            degrees_c=1.23456,
            thermometer=self.thermometer
        )
        with transaction.atomic():
            temp.save()
        serializer = TemperatureReadingSerializer(
            temp, context=self.context
        )
        self.assertEqual(temp.id, serializer.data['id'])
        self.assertEqual(temp.degrees_c, float(serializer.data['degrees_c']))
        self.assertEqual(temp.thermometer.display_name, serializer.data['thermometer'])
