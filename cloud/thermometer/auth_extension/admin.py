from django.contrib import admin


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfiles

    Fields:
        user: one2one relationship with user model
        created_date: date profile was created
        time_zone: user's time zone

    References:
        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User

    """

    fieldsets = (
        ('User', {'fields': ('user',)},),
        ('Profile Information', {
            'fields': ('created_date', 'time_zone')})
    )
    list_display = ('user', 'time_zone', 'created_date')
    list_filter = ('created_date', 'time_zone')
