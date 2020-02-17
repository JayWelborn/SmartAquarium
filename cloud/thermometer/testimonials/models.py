from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# Create your models here.
class Testimonial(models.Model):
    """Model to store User submitted product testimonials

    Fields:
        user: User who submitted the testimonial
        submission_date: Date testimonial was submitted
    """

    user = models.ForeignKey(
        get_user_model(),
        related_name='testimonials',
        on_delete=models.CASCADE
    )

    submission_date = models.DateTimeField(
        default=timezone.now
    )

    testimonial = models.TextField()
