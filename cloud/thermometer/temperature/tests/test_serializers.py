import re

from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.test import APITestCase

from temperature.models import Thermometer, TemperatureReading
from temperature.serializers import TemperatureReadingSerializer, ThermometerSerializer


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
        create_valid_data: Serializer should accept valid data to create new thermometer
        create_invalid_data: Serializer should reject invalid data
        update_add_temperatures: Passing new temperatures to a serializer with an existing instance
            should create new corresponding temperature records
    """

    def setUp(self):
        """
        create test data
        """
        self.user = get_user_model().objects.create_user(
            username='test',
            password='testingpass',
            email='test@e.mail'
        )
        self.test_thermometer = Thermometer.objects.create(
            display_name='test thermometer'
        )
        self.context = {'request': None}

    def tearDown(self):
        """
        delete test data
        """
        for therm in Thermometer.objects.all():
            therm.delete()
        for user in get_user_model().objects.all():
            user.delete()

    def test_create_valid_data(self):
        """
        Serializer should accept valid data and create a new thermometer with no owner or
        temperature readings associated.
        """
        valid_data = {
            'display_name': 'testy thermometer',
        }
        serializer = ThermometerSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        new_therm = serializer.save()
        self.assertEquals(new_therm.display_name, valid_data['display_name'])
        self.assertEquals(len(new_therm.temperatures.all()), 0)

        valid_data = {
            'display_name': 'testy thermometer2',
            'temperatures': []
        }
        serializer = ThermometerSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        new_therm = serializer.save()
        self.assertEquals(new_therm.display_name, valid_data['display_name'])
        self.assertEquals(len(new_therm.temperatures.all()), 0)

        serializer = ThermometerSerializer(data={})
        self.assertTrue(serializer.is_valid())
        new_therm = serializer.save()
        self.assertTrue(re.match(r'Smart Thermometer \d+', new_therm.display_name))
        self.assertEquals(len(new_therm.temperatures.all()), 0)

    def test_create_invalid_data(self):
        """
        Thermometers should not be able to be created with temperature records.
        """
        invalid_data = {
            'display_name': 'invalid!!!',
            'temperatures': [
                {'degrees_c': 101},
            ]
        }
        serializer = ThermometerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('temperatures', serializer.errors)
        self.assertEquals(str(serializer.errors['temperatures'][0]),
            'New Thermometers cannot be created with temperature readings'
        )

    def test_update_add_temperatures(self):
        """
        Passing new temperature values to serializer with existing instance should create new
        temperature readings linked to instance.
        """
        self.test_thermometer.register(self.user)
        self.assertIs(self.test_thermometer.owner, self.user)
        expected_temps = [28, 21, 22]
        data = {
            'temperatures': [
                {'degrees_c': expected_temps[0]},
                {'degrees_c': expected_temps[1]},
                {'degrees_c': expected_temps[2]},
            ]
        }
        serializer = ThermometerSerializer(
            self.test_thermometer, data=data, context=self.context, partial=True
        )
        self.assertTrue(serializer.is_valid())
        thermometer = serializer.save()
        self.assertEquals(thermometer.display_name, 'test thermometer')
        self.assertIs(thermometer.owner, self.user)
        self.assertEquals(len(thermometer.temperatures.all()), 3)
        temps = thermometer.temperatures.all().order_by('time_recorded')
        for i in range(len(expected_temps)):
            self.assertEquals(temps[i].degrees_c, expected_temps[i])

        self.assertEquals(len(TemperatureReading.objects.all()), 3)
