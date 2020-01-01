from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse

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
        })
        self.detailview = TemperatureReadingViewset.as_view({
            'get': 'retrieve',
        })

    def tearDown(self):
        """
        Clear test database
        """
        for user in get_user_model().objects.all():
            with transaction.atomic():
                user.delete()

        self.assertEqual(len(TemperatureReading.objects.all()), 0)
        self.assertEqual(len(Thermometer.objects.all()), 0)

    def test_unauthenticated_user_permissions(self):
        """
        Unauthenticated users should not be able to view, create, edit, or delete temperature
        readings
        """
        self.client.logout()

        # list view
        url = reverse('temperaturereading-list')
        request = self.factory.get(url)
        response = self.listview(request)
        self.assertEquals(response.status_code, 403)

        request = self.factory.post(url, {'degrees_c': 23})
        response = self.listview(request)
        self.assertEquals(response.status_code, 403)

        # detail view
        for temp in self.thermometer.temperatures.all():
            url = reverse('temperaturereading-detail', args=[temp.pk])
            request = self.factory.get(url)
            response = self.detailview(request, pk=temp.pk)
            self.assertEquals(response.status_code, 403)

            data = {
                'degrees_c': 12
            }
            request = self.factory.put(url, data=data, partial=True)
            response = self.detailview(request)
            self.assertEqual(response.status_code, 403)

            request = self.factory.delete(url)
            response = self.detailview(request)
            self.assertEqual(response.status_code, 403)
