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
        test_unauthenticated_user_permissions: Unauthenticated users should not be able to view,
            create, edit, or delete temperature readings
        test_authenticated_get: Users should be able to see their own temperature readings
            Staff should be able to see all temperature readings
        test_authenticated_post: Viewset should not allow post requests
    
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
        with transaction.atomic():
            self.thermometer.save()
        for i in range(10):
            temp = TemperatureReading(
                degrees_c=i,
                thermometer=self.thermometer
            )
            with transaction.atomic():
                temp.save()
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

    def test_authenticated_get(self):
        """
        Users should be able to see their own temperature readings
        Staff should be able to see all temperature readings
        """
        # owner should see all temps created
        url = reverse('temperaturereading-list')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.listview(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), len(TemperatureReading.objects.all()))

        # new user should see no temps
        user = get_user_model().objects.create_user(
            username='new',
            password='newpass',
            email='em@a.il'
        )
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        response = self.listview(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 0)

        # giving new user a thermometer with a temp should get 1 temp on get
        therm = Thermometer()
        therm.register(user)
        temp = TemperatureReading(thermometer=therm, degrees_c=1)
        with transaction.atomic():
            temp.save()
        
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        response = self.listview(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)

        superuser = get_user_model().objects.create_superuser(
            username='superuser',
            password='newpass',
            email='super@email.it'
        )

        request = self.factory.get(url)
        force_authenticate(request, user=superuser)
        response = self.listview(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 11)

    def test_authenticated_post(self):
        """
        post to temperature reading viewset should not create new readings.
        """
        url = reverse('temperaturereading-list')
        data = {
            'degrees_c': 1,
        }
        request = self.factory.post(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = self.listview(request)
        self.assertEquals(response.status_code, 405)
        self.assertEquals(str(response.data['detail']), 'Method "POST" not allowed.')

    def test_authenticated_put(self):
        """
        Put reqeusts should not be allowed
        """
        temp = TemperatureReading(degrees_c=1, thermometer=self.thermometer)
        with transaction.atomic():
            temp.save()
        url = reverse('temperaturereading-detail', args=[temp.pk])
        data = {'degrees_c': 2}

        request = self.factory.put(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = self.detailview(request)
        self.assertEquals(response.status_code, 405)
        self.assertEquals(str(response.data['detail']), 'Method "PUT" not allowed.')

    def test_authenticated_delete(self):
        """
        Delete requests should not be allowed
        """
        temp = TemperatureReading(degrees_c=1, thermometer=self.thermometer)
        with transaction.atomic():
            temp.save()
        url = reverse('temperaturereading-detail', args=[temp.pk])
        request = self.factory.delete(url, args=[temp.pk])
        force_authenticate(request, self.user)
        response = self.detailview(request, pk=temp.pk)
        self.assertEquals(response.status_code, 405)
        self.assertEquals(str(response.data['detail']), 'Method "DELETE" not allowed.')



class ThermometerViewsetTests(APITestCase):
    """Tests for Thermometer Viewset

    Methods:
        setUp: Create test data
        tearDown: Empty test database
        test_unauthenticated_requests: All unauthenticated requests should fail
        test_authenticated_get: Regular users should be able to see only their own thermometers.
            Staff should see all thermometers
    """

    def setUp(self):
        """
        create test data
        """
        self.normal_user = get_user_model().objects.create_user(
            username='normal',
            password='user',
            email='normal@user.com'
        )
        self.super_user = get_user_model().objects.create_superuser(
            username='super',
            password='user',
            email='super@user.com'
        )
        self.therm = Thermometer(display_name='test thermometer')
        self.therm.register(self.normal_user)
        self.factory = APIRequestFactory()
        self.listview = ThermometerViewset.as_view({
            'get': 'list',
            'post': 'create'
        })
        self.detailview = ThermometerViewset.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })
    
    def tearDown(self):
        """
        empty test database
        """
        with transaction.atomic():
            for user in get_user_model().objects.all():
                user.delete()
        
        self.assertEquals(len(get_user_model().objects.all()), 0)
        self.assertEquals(len(Thermometer.objects.all()), 0)
        self.assertEquals(len(TemperatureReading.objects.all()), 0)

    def test_unauthenticated_requests(self):
        """
        This viewset should reject all unauthenticated requests
        """
        self.client.logout()

        # ListView requests
        url = reverse('thermometer-list')
        request = self.factory.get(url)
        response = self.listview(request)
        self.assertEquals(response.status_code, 403)

        data = {'display_name': 'fred'}
        requet = self.factory.post(url, data)
        response = self.listview(request)
        self.assertEquals(response.status_code, 403)

        # DetailView requests
        url = reverse('thermometer-detail', args=[self.therm.pk])
        request = self.factory.get(url)
        response = self.detailview(request, pk=self.therm.pk)
        self.assertEquals(response.status_code, 403)
    
        data = {'display_name': 'forky'}
        request = self.factory.patch(url, data=data, partial=True)
        response = self.detailview(request)
        self.assertEquals(response.status_code, 403)

        data['therm_id'] = 'sausage'
        request = self.factory.put(url, pk=self.therm.pk, data=data)
        response = self.detailview(request)
        self.assertEquals(response.status_code, 403)

        request = self.factory.delete(url, pk=self.therm.pk)
        response = self.detailview(request)
        self.assertEquals(response.status_code, 403)

    def test_authenticated_get(self):
        """
        Regular users should be able to see their own thermometers
        Staff should be able to see all thermometers
        """
        other_user = get_user_model().objects.create_user(
            username="other",
            password="otherpass",
            email="e@mail.mil"
        )
        normal_user_therms = []
        for i in range(4):
            therm = Thermometer()
            therm.register(self.normal_user)
            normal_user_therms.append(therm)
        
        other_user_therms = []
        for i in range(4):
            therm = Thermometer()
            therm.register(other_user)
            other_user_therms = []

        normal_user_therms.append(self.therm)

        # Test list view
        url = reverse('thermometer-list')
        request = self.factory.get(url)
        force_authenticate(request, user=self.normal_user)
        response = self.listview(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 5)
        for therm_data in response.data:
            therm = Thermometer.objects.get(therm_id=therm_data['therm_id'])
            self.assertIn(therm, normal_user_therms)

        request = self.factory.get(url)
        force_authenticate(request, user=self.super_user)
        response = self.listview(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 9)

        # Test detail view
        url = reverse('thermometer-detail', args=[self.therm.pk])
        request = self.factory.get(url)
        force_authenticate(request, self.normal_user)
        response = self.detailview(request, pk=self.therm.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['owner'][-2], str(self.normal_user.pk))

        request = self.factory.get(url)
        force_authenticate(request, self.super_user)
        response = self.detailview(request, pk=self.therm.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['owner'][-2], str(self.normal_user.pk))
