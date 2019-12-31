from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from temperature.models import TemperatureReading, Thermometer
from temperature.viewsets import TemperatureReadingViewset, ThermometerViewset


class TemperatureReadingViewsetTests(APITestCase):
    """Tests for TemperatureReading Viewset.

    Methods:
        setUp: Create test data
        tearDown: Clear test database
    
    """
    def setUp(self):
        """
        Create test objects
        """
        self.user = get_user_model().objects.create_user(
            username='test user',
            password='testpass',
            email='test@e.mail'
        )
        self.thermometer = Thermometer.objects.create(
            display_name='test thermometer'
        )
        self.thermometer.register(self.user)
        for i in range(10):
            temp = TemperatureReading(
                degrees_c=i,
                thermometer=self.thermometer
            )
        self.factory = APIRequestFactory()
        self.listview = TemperatureReadingViewset.as_view({
            'get': 'list',
            'post': 'create'
        })
        self.detailview = TemperatureReadingViewset.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })

    def tearDown(self):
        """
        Clear test database
        """
        for user in get_user_model().objects.all():
            with transaction.atomic():
                user.delete()

    def test_nothing(self):
        """
        test nothing other than that tests are running
        """
        self.assertIs(self.user, self.thermometer.owner)
