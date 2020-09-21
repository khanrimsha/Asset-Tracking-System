from django.contrib import admin
from .models import Location
from leaflet.admin import LeafletGeoAdmin
# Register your models here.
class LocationAdmin(LeafletGeoAdmin):
    list_display=('name','lat','long')

admin.site.register(Location,LocationAdmin)
class Meta:
    verbose_name_plural='Location'