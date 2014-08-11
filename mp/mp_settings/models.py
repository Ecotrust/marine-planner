from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify

class MarinePlannerSettings(models.Model):
    active = models.BooleanField(default=False, help_text='Only 1 project can be active at any time.')
    project_name = models.CharField(max_length=75, blank=True, null=True, help_text='If there is no entry for Project Logo, your Project Name will be displayed at the top-left of the screen.')
    slug_name = models.CharField(max_length=75, blank=True, null=True, help_text='This Slug Name can be used in the URL to distinguish one project from another (/my_slug/planner or /my_slug/catalog).')
    table_of_contents = models.ForeignKey('data_manager.TOC', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    zoom = models.IntegerField(blank=True, null=True)
    min_zoom = models.IntegerField(blank=True, null=True, default=5, help_text='Minimum Zoom Level (5 is default).')
    max_zoom = models.IntegerField(blank=True, null=True, default=12, help_text='Maximum Zoom Level (12 is default).')
    default_hash = models.TextField(blank=True, null=True, help_text="Default Map View as expressed in the URL hash (should start with '#x=')")
    project_logo = models.CharField(max_length=255, blank=True, null=True, help_text='Either a relative path within your media directory or a valid URL.')
    project_icon = models.CharField(max_length=255, blank=True, null=True, help_text='Either a relative path within your media directory or a valid URL.')
    project_home_page = models.URLField(max_length=255, blank=True, null=True, help_text='The Project Name or Project Logo will link to this page.')
    enable_drawing = models.BooleanField(default=False, help_text='Click to enable the Designs tab with Drawing for authenticated users.')
    bitly_registered_domain = models.URLField(max_length=255, blank=True, null=True)
    bitly_username = models.CharField(max_length=75, blank=True, null=True)
    bitly_api_key = models.CharField(max_length=75, blank=True, null=True)
        
    @property
    def slug(self):
        return slugify(self.project_name)
    
    def save(self, *args, **kwargs):
        self.slug_name = self.slug
        super(MarinePlannerSettings, self).save(*args, **kwargs)
        if self.active and MarinePlannerSettings.objects.filter(active=True).count() > 1:
            # Ensure that any previously active study region is deactivated
            # There can be only one!
            MarinePlannerSettings.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
           