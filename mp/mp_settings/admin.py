from django.contrib import admin
from models import MarinePlannerSettings 

class MarinePlannerSettingsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'latitude', 'longitude', 'zoom', 'active')
    search_fields = ['project_name']
    ordering = ('project_name',)
    exclude = ['slug_name']

admin.site.register(MarinePlannerSettings, MarinePlannerSettingsAdmin)
