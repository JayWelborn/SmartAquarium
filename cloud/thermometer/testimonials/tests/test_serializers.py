from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework.test import APITestCase

from testimonials.models import Testimonial
from testimonials.serializers import TestimonialSerializer


class TestimonialSerializerTests(APITestCase):
    """Tests for Testimonial Serializer

    Methods:
        setUp: Create test data
        tearDown: Clean test database
        create_valid_data: Serializer presented with valid data should create new testimonial record
            on save
        create_invalid_data: Presenting invalid data, such as no text, should result in serializer
            being invalid
    """

    def setUp(self):
        """
        Create test data
        """
        self.user = get_user_model().objects.create_user(
            username='test',
            password='password',
            email='test@e.mail'
        )
        self.context = {'request': None}
        self.now = timezone.now()

    def tearDown(self):
        """
        Clean test database
        """
        for user in get_user_model().objects.all():
            user.delete()

    def test_create_valid_data(self):
        """
        Serializer presented with valid data should create new testimonial record on save
        """
        valid_datasets = (
            {
                'user': self.user,
                'text': 'This is my testimonial. It can be as long as I want it to be, or as ' + \
                        'short as I desire',
            },
            {
                'user': self.user,
                'text': 'some text',
                'submission_date': (self.now - timedelta(days=3)).isoformat()
            }
        )
        for valid_data in valid_datasets:
            serializer = TestimonialSerializer(data=valid_data)
            self.assertTrue(serializer.is_valid())
            with transaction.atomic():
                testimonial = serializer.save(user=valid_data['user'])
            self.assertEquals(testimonial.user.pk, valid_data['user'].pk)
            self.assertEquals(testimonial.text, valid_data['text'])
            if 'submission_date' in valid_data:
                self.assertEquals(
                    testimonial.submission_date.isoformat(), valid_data['submission_date']
                )

    def test_create_invalid_data(self):
        """
        Presenting invalid data, such as no text, should result in serializer being invalid
        """
        datasets = (
            {},
            {'text': None},
            {
                'text': 'yes text',
                'submission_date': 'not a date'
            },
            {
                'text': 'text',
                'submission_date': self.now.isoformat()[1:]
            }
        )
        for dataset in datasets:
            serializer = TestimonialSerializer(data=dataset)
            self.assertFalse(serializer.is_valid())

    def test_serialize_existing_instance(self):
        """
        Serializing an existing instance should convert values to JSON as expected
        """
        testimonial = Testimonial(user=self.user, text='Test Text', submission_date=self.now)
        serializer = TestimonialSerializer(
            testimonial, context=self.context
        )
        self.assertEquals(serializer.data['user'], f'/users/{self.user.pk}/')
        self.assertEquals(serializer.data['submission_date'], self.now.isoformat().replace('+00:00', 'Z'))
        self.assertEquals(serializer.data['text'], 'Test Text')

  