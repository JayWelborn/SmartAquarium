import uuid

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
        test_authenticated_post_valid: POST requests should create a new thermometer record
            registered to the authenticated user
        test_authenticated_post_invalid_data: POST requests with invalid data should return http
            code 400 bad request
        test_authenticated_put_valid_data: PUT requests should update all fields on an existing
            model
        test_authenticated_put_invalid_data: Invalid data in PUT requests should return 400
        test_authenticated_path_valid_data: PATCH requests should update the correct fields
        test_authenticated_path_invalid_data: PATCH requests with invalid data should return 400
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

    def test_authenticated_post_valid(self):
        """
        POST requests should create a new thermometer registered to the current user
        """
        def make_assertions_about_data(data, user):
            url = reverse('thermometer-list')
            request = self.factory.post(url, data=data, format='json')
            force_authenticate(request, user=user)
            response = self.listview(request)
            self.assertEquals(response.status_code, 201)
            self.assertEquals(int(response.data['owner'][-2]), user.pk)
            self.assertEquals(response.data['display_name'], data['display_name'])
            self.assertEquals(response.data['therm_id'], str(data['therm_id']))
        
        data = {
            'display_name': 'new thermometer',
            'therm_id': uuid.uuid4()
        }
        make_assertions_about_data(data, self.normal_user)

        data = {
            'display_name': 'newer thermometer',
            'therm_id': uuid.uuid4()
        }
        make_assertions_about_data(data, self.super_user)

    def test_authenticated_post_invalid_data(self):
        """
        POST requests with invalid data should return error code
        """
        def make_assertions_with_data(data):
            url = reverse('thermometer-list')
            request = self.factory.post(url, data=data, format='json')
            force_authenticate(request, user=self.normal_user)
            response = self.listview(request)
            self.assertEquals(response.status_code, 400)
        
        data_sets = [
            {
                'temperatures': [
                    {'degrees_c': 91}
                ]
            },
            {
                'display_name': 'thisnameiswaytoolongandwonteverbeacceptedbecausethelongestallowedis75characters'
            },
            {
                'display_name': 'valid',
                'temperatures': [{'degrees_c': 40}]
            }
        ]
        for data in data_sets:
            make_assertions_with_data(data)
    
    def test_authenticated_put_valid_data(self):
        """
        Authenticated put requests with valid data should overwrite existing records with
        new values
        """
        def validate_put_request(data):
            url = reverse('thermometer-detail', args=[self.therm.pk])
            request = self.factory.put(url, data=data, format='json')
            force_authenticate(request, self.normal_user)
            response = self.detailview(request, data=data, pk=self.therm.pk)
            self.therm = Thermometer.objects.get(pk=self.therm.pk)
            self.assertEquals(response.status_code, 200)

            if 'temperatures' in data.keys():
                for temp in data['temperatures']:
                    temp = TemperatureReading.objects.get(degrees_c=temp['degrees_c'])
                    self.assertIsNotNone(temp)
                    self.assertEquals(temp.thermometer.pk, self.therm.pk)
                del data['temperatures']

            for key, value in data.items():
                self.assertEquals(getattr(self.therm, key), value)
                self.assertIn(key, response.data)

        data_sets = [
            {
                'display_name': 'new display name',
                'therm_id': uuid.uuid4()
            },
            {
                'display_name': 'newer display name',
                'therm_id': uuid.uuid4()
            },
            {
                'display_name': 'newest display name',
                'therm_id': uuid.uuid4()
            },
            {
                'temperatures': [
                    {'degrees_c': 1},
                    {'degrees_c': 2},
                    {'degrees_c': 4},
                    {'degrees_c': 5},
                ]
            }
        ]

        for data in data_sets:
            validate_put_request(data)

    def test_authenticated_put_invalid_data(self):
        """
        PUT requests with invalid data should return 400
        """
        url = reverse('thermometer-detail', args=[self.therm.pk])
        new_therm = Thermometer(therm_id='1')
        
        def put_invalid_data(data):
            request = self.factory.put(url, data=data, format='json')
            force_authenticate(request, user=self.normal_user)
            response = self.detailview(request, data=data, pk=self.therm.pk)
            self.assertEquals(response.status_code, 400)

        datasets = [
            {
                'therm_id': 'apweoriulsadk falk4;l43aklk jea;lkj34leskrjng lksjn435lka345asdn lksjd'
            },
            {
                'display_name': 'thisnameiswaytoolongandwonteverbeacceptedbecausethelongestallowedis75characters'
            },
            {
                'therm_id': '1'
            },
            {
                'temperatures': [{'degrees_c': 123456789012334567}]
            }
        ]

        for data in datasets:
            put_invalid_data(data)

    def test_authenticated_patch_valid_data(self):
        """
        Authenticated patch requests with valid data should overwrite existing records with
        new values
        """
        def validate_patch_request(data):
            url = reverse('thermometer-detail', args=[self.therm.pk])
            request = self.factory.patch(url, data=data, format='json')
            force_authenticate(request, self.normal_user)
            response = self.detailview(request, data=data, pk=self.therm.pk)
            self.therm = Thermometer.objects.get(pk=self.therm.pk)
            self.assertEquals(response.status_code, 200)

            if 'temperatures' in data.keys():
                for temp in data['temperatures']:
                    temp = TemperatureReading.objects.get(degrees_c=temp['degrees_c'])
                    self.assertIsNotNone(temp)
                    self.assertEquals(temp.thermometer.pk, self.therm.pk)
                del data['temperatures']

            for key, value in data.items():
                self.assertEquals(getattr(self.therm, key), value)
                self.assertIn(key, response.data)

        data_sets = [
            {
                'display_name': 'new display name',
            },
            {
                'therm_id': uuid.uuid4()
            },
            {
                'display_name': 'newest display name',
                'therm_id': uuid.uuid4()
            },
            {
                'temperatures': [
                    {'degrees_c': 1},
                    {'degrees_c': 2},
                    {'degrees_c': 4},
                    {'degrees_c': 5},
                ]
            }
        ]

        for data in data_sets:
            validate_patch_request(data)

    def test_authenticated_patch_invalid_data(self):
        """
        PATCH requests with invalid data should return 400
        """
        url = reverse('thermometer-detail', args=[self.therm.pk])
        new_therm = Thermometer(therm_id='1')
        
        def patch_invalid_data(data):
            request = self.factory.patch(url, data=data, format='json')
            force_authenticate(request, user=self.normal_user)
            response = self.detailview(request, data=data, pk=self.therm.pk)
            self.assertEquals(response.status_code, 400)

        datasets = [
            {
                'therm_id': 'apweoriulsadk falk4;l43aklk jea;lkj34leskrjng lksjn435lka345asdn lksjd'
            },
            {
                'display_name': 'thisnameiswaytoolongandwonteverbeacceptedbecausethelongestallowedis75characters'
            },
            {
                'therm_id': '1'
            },
            {
                'temperatures': [{'degrees_c': 123456789012334567}]
            }
        ]

        for data in datasets:
            patch_invalid_data(data)

    def test_delete(self):
        """
        Normal users should be able to delete their thermometers. Superusers should be able to
        delete anyone's thermometers
        """
        second_therm = Thermometer.objects.create()
        second_therm.register(self.normal_user)

        # normal user delete their own thermometer
        url = reverse('thermometer-detail', args=[second_therm.pk])
        request = self.factory.delete(url)
        force_authenticate(request, self.normal_user)
        response = self.detailview(request, pk=second_therm.pk)
        self.assertEquals(response.status_code, 204)
        try:
            Thermometer.objects.get(pk=second_therm.pk)
            self.fail("Query should fail, as oject should no longer exist")
        except Thermometer.DoesNotExist as dne:
            self.assertEquals(str(dne), "Thermometer matching query does not exist.")

        # normal user delete others thermometer
        second_therm = Thermometer.objects.create()
        second_therm.register(self.super_user)
        url = reverse('thermometer-detail', args=[second_therm.pk])
        request = self.factory.delete(url)
        force_authenticate(request, self.normal_user)
        response = self.detailview(request, pk=second_therm.pk)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Thermometer.objects.get(owner=self.super_user).pk, second_therm.pk)

        # superuser delete other's thermometer
        url = reverse('thermometer-detail', args=[self.therm.pk])
        request = self.factory.delete(url)
        force_authenticate(request, self.super_user)
        response = self.detailview(request, pk=self.therm.pk)
        self.assertEquals(response.status_code, 204)
        try:
            Thermometer.objects.get(pk=self.therm.pk)
            self.fail("Query should fail, as oject should no longer exist")
        except Thermometer.DoesNotExist as dne:
            self.assertEquals(str(dne), "Thermometer matching query does not exist.")

        # superuser delete own thermometer
        url = reverse('thermometer-detail', args=[second_therm.pk])
        request = self.factory.delete(url)
        force_authenticate(request, self.super_user)
        response = self.detailview(request, pk=second_therm.pk)
        self.assertEquals(response.status_code, 204)
        try:
            Thermometer.objects.get(pk=second_therm.pk)
            self.fail("Query should fail, as oject should no longer exist")
        except Thermometer.DoesNotExist as dne:
            self.assertEquals(str(dne), "Thermometer matching query does not exist.")
