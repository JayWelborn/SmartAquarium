from django.contrib import admin

from .models import TemperatureReading

# Register your models here.
class TemperatureReadingInline(admin.TabularInline):
    """Tabular inline formset for Temperature Readings

    Fields:
        degrees_c: degrees Celsius of temperature reading
        time_recorded: time reading was taken

    """
    model = TemperatureReading


class ThermometerAdmin(admin.ModelAdmin):
    """Admin interface for Thermomter

    Fields:
        owner: user who owns this thermometer
        therm_id: UUID for the thermometer
        display_name: thermometers display name
        created_date: date the thermometer was created
        registered: whether or not this thermometer has been registered by a user
        registration_date: date thermometer was registered

    """

    fieldsets = (
        ('Thermometers', {
            'fields': (
                'therm_id',
                'owner',
                'display_name',
                'created_date',
                'registration_date'
            ),
        }),
    )
    readonly_fields = ('therm_id',)
    inlines = (TemperatureReadingInline,)
    list_display = ('owner', 'display_name', 'therm_id', 'created_date', 'registration_date')
    list_filter = ('created_date', 'registration_date')
