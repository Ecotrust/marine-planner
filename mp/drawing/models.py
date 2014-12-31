from django.db import models
from django.utils.html import escape
from madrona.features import register
from madrona.features.models import PolygonFeature
from general.utils import sq_meters_to_sq_miles

@register
class AOI(PolygonFeature):
    description = models.TextField(null=True,blank=True)
    
    @property
    def formatted_area(self):
        return int((self.area_in_sq_miles * 10) +.5) / 10.
     
    @property
    def area_in_sq_miles(self):
        return sq_meters_to_sq_miles(self.geometry_final.area)
        
    @property
    def serialize_attributes(self):
        from general.utils import format
        attributes = []
        if self.description: 
            attributes.append({'title': 'Description', 'data': self.description})
        attributes.append({'title': 'Area', 'data': '%s sq miles' %format(self.area_in_sq_miles, 2)})
        return { 'event': 'click', 'attributes': attributes }
    
    @classmethod
    def fill_color(self):
        return '776BAEFD'      
    
    @classmethod
    def outline_color(self):
        return '776BAEFD'    

    def clipToGrid(self):        
        print 'clipping...'

        from scenarios.models import GridCell
        from django.contrib.gis.db.models.aggregates import Union
        geom = self.geometry_orig
        intersection = GridCell.objects.filter(centroid__intersects=geom)
        new_shape = intersection.aggregate(Union('geometry'))
        return new_shape['geometry__union']

    def save(self, *args, **kwargs):
        self.geometry_final = self.clipToGrid()
        # if self.geometry_final:
        #     self.geometry_final = clean_geometry(self.geometry_final)
        super(AOI, self).save(*args, **kwargs) # Call the "real" save() method   

    class Options:
        verbose_name = 'Area of Interest'
        icon_url = 'img/aoi.png'
        export_png = False
        manipulators = []
        # manipulators = ['drawing.manipulators.ClipToPlanningGrid']
        # optional_manipulators = ['clipping.manipulators.ClipToShoreManipulator']
        form = 'drawing.forms.AOIForm'
        form_template = 'aoi/form.html'
        show_template = 'aoi/show.html'
