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
        
        self.thermometer = Thermometer(
            display_name='therm'
        )

        self.temps = []
        for i in range(50):
            self.temps.append(
                TemperatureReading(
                    thermometer=self.thermometer,
                    degrees_c=i
                )
            )
        self.assertEqual(50, len(self.temps))

        with transaction.atomic():
            self.user.save()
            self.thermometer.register(self.user)
            for temp in self.temps:
                temp.save()
        
        self.context = {'request': None}

    def tearDown(self):
        """
        clear test database
        """
        with transaction.atomic():
            self.user.delete()
        
        self.assertEqual(0, len(TemperatureReading.objects.all()))
        self.assertEqual(0, len(get_user_model().objects.all()))
        self.assertEqual(0, len(Thermometer.objects.all()))
        

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

    def test_update_raises_type_error(self):
        """
        Update method should always raise type error.
        """
        temp = self.temps[0]
        valid_data = {
            'degrees_c': 101
        }
        valid_data_bigger = {
            'degrees_c': 100,
            'thermometer': 'display'
        }
        invalid_data = {
            'degrees_c': 'snacks',
            'thermometer': 'invalid'
        }

        serializer = TemperatureReadingSerializer(
            temp, data=valid_data, context=self.context, partial=True
        )
        self.assertTrue(serializer.is_valid())
        try:
            serializer.save()
            self.fail("Saving update should fail - valid data")
        except TypeError as te:
            exp = "Updating Temperature Readings via API not allowed. " + \
                  "Contact a system administrator for assistance."
            self.assertEquals(exp, str(te))
            
        serializer = TemperatureReadingSerializer(
            temp, data=valid_data_bigger, context=self.context, partial=True
        )
        self.assertTrue(serializer.is_valid())
        try:
            serializer.save()
            self.fail("Saving update should fail - valid data")
        except TypeError as te:
            exp = "Updating Temperature Readings via API not allowed. " + \
                  "Contact a system administrator for assistance."
            self.assertEquals(exp, str(te))

        serializer = TemperatureReadingSerializer(
            temp, data=invalid_data, context=self.context, partial=True
        )
        self.assertFalse(serializer.is_valid())


class ThermometerSerializerTests(APITestCase):
    """Tests for Thermometer Serializer

    Methods:
        setUp: create test data
        tearDown: clean test database
        serializer_accepts_valid_data: Serializer should accept

    """
