from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from timezone_field import TimeZoneField


class UserProfile(models.Model):
    """Model to store extra info about each User

    Fields:
        user: 1-1 relationship with User used for auth
        created_date: date profile was created
        time_zone: user's time zone (default UTC)

    References:
        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User
        * https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
        * https://github.com/mfogel/django-timezone-field
        * https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    """

    class Meta:
        verbose_name: 'Profile'
        verbose_name_plural: 'Profiles'

    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(
        default=timezone.now
    )

    time_zone = TimeZoneField(default='UTC')


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

