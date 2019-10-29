from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase

import pytz

from auth_extension.models import UserProfile


class UserProfileModelTests(TestCase):
    """Tests for UserProfile model

    Methods:

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/

    """

    def setUp(self):
        """
        Create instance(s) for tests
        """
        self.UserModel = get_user_model()
        self.test_user_one = self.UserModel.objects.create_user(
            username='test one',
            password='password',
            email='test1@test.com'
        )
        self.test_user_two = self.UserModel.objects.create_user(
            username='test two',
            password='password',
            email='test2@test.com'
        )
        self.test_profile = self.test_user_one.profile

    def tearDown(self):
        """
        Empty Test Database between tests
        """
        for user in self.UserModel.objects.all():
            user.delete()

        user_set = self.UserModel.objects.all()
        self.assertFalse(user_set)
        profile_set = UserProfile.objects.all()
        self.assertFalse(profile_set)


    def test_create_delete_user_affects_profile(self):
        """
        Creating a user should create an associated profile via
        post-save signal handling
        """
        self.assertTrue(self.test_profile)
        new_user = self.UserModel.objects.create_user(
            username='throwaway',
            password='password',
            email='throwaway@testing.test'
        )
        new_profile = new_user.profile
        self.assertTrue(new_profile)
        self.assertIs(new_profile.user, new_user)
        new_profile = UserProfile.objects.get(user=new_user)
        self.assertTrue(new_profile)
        self.assertEqual(new_profile.user, new_user)
        new_user.delete()
        try:
            new_profile = UserProfile.objects.get(user=new_user)
            self.fail("Query should fail. Deleting user should have deleted profile")
        except:
            pass

    def test_default_timezone(self):
        """
        Timezone should default to UTC
        """
        tz = self.test_profile.time_zone
        self.assertEqual(tz, pytz.UTC)

    def test_profile_set_timezone(self):
        """
        Timezone should be settable to any pytz timezone
        """
        for tz in pytz.all_timezones:
            self.test_profile.time_zone = tz
            # force TimeZoneField to validate
            with transaction.atomic():
                self.test_profile.save()
            self.assertEquals(tz, self.test_profile.time_zone)
            self.assertEquals(tz, self.test_user_one.profile.time_zone)

    def test_profile_ignores_weird_timezones(self):
        """
        Timezone should ignore invalid values
        """
        try:
            self.test_profile.time_zone = "Lemon"
            # Should fail
            with transaction.atomic():
                self.test_profile.save()
        except ValidationError as ve:
            self.assertEquals(ve.message, "Invalid timezone 'Lemon'")
