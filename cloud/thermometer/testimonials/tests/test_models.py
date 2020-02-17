import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import TestCase
from django.utils import timezone

from testimonials.models import Testimonial


class TestimonialModelTests(TestCase):
    """
    Tests for testimonial model
    """

    def setUp(self):
        self.UserModel = get_user_model()
        self.test_user = self.UserModel.objects.create_user(
            username='testy',
            password='passy',
            email='e@mai.lcom'
        )
        self.today = timezone.now().date()

    def tearDown(self):
        for user in self.UserModel.objects.all():
            user.delete()

        self.assertFalse(self.UserModel.objects.all())
        self.assertFalse(Testimonial.objects.all())

    def test_submission_date(self):
        """
        Default submission date should be today.
        Overrides should be honored
        """
        mony = Testimonial(user=self.test_user)
        with transaction.atomic():
            mony.save()
        self.assertEqual(self.today, mony.submission_date.date())

        yesterday = self.today - datetime.timedelta(days=1)
        mony = Testimonial(user=self.test_user, submission_date=yesterday)
        with transaction.atomic():
            mony.save()
        self.assertEqual(mony.submission_date, yesterday)
  