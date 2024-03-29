from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from auth_extension.admin import UserProfileAdmin
from auth_extension.models import UserProfile

from temperature.admin import ThermometerAdmin
from temperature.models import Thermometer

from testimonials.admin import TestimonialAdmin
from testimonials.models import Testimonial


class CustomAdmin(AdminSite):
    """Admin site with customized header

    References:
        * https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#customizing-the-adminsite-class
    
    """
    site_header = 'Thermometer Administration'
    site_title = 'Thermometer Administration'


admin_site = CustomAdmin()
admin_site.register(get_user_model())
admin_site.register(Group)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Thermometer, ThermometerAdmin)
admin_site.register(Testimonial, TestimonialAdmin)
