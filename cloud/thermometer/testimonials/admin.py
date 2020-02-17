from django.contrib import admin


# Register your models here.
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for Testimonials

    Fields:
        user: user who submitted the testimonial
        submission_date: date testimonial was submitted
        testimonial: actual testimonial text

    References:
        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User

    """
    list_display = ('user', 'submission_date')
    fields = ('user', 'submission_date', 'text')
