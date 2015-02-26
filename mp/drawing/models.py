from django.db import models
from django.utils.html import escape
from madrona.features import register
from madrona.features.models import PolygonFeature
from madrona.common.utils import LargestPolyFromMulti
from general.utils import sq_meters_to_sq_miles, format_precision
from ofr_manipulators import clip_to_grid, intersecting_cells
from reports import get_summary_reports

@register
class AOI(PolygonFeature):
    description = models.TextField(null=True,blank=True)
    
    @property
    def formatted_area(self):
        return int((self.area_in_sq_miles * 10) +.5) / 10.
     
    @property
    def area_in_sq_miles(self):
        return sq_meters_to_sq_miles(self.geometry_final.area)

    def summary_reports(self, attributes):
        # Call get_summary_reports with intersecting Grid Cells 
        grid_cells = intersecting_cells(self.geometry_orig)
        get_summary_reports(grid_cells, attributes)
        
        
    @property
    def serialize_attributes(self):
        attributes = []
        if self.description: 
            attributes.append({'title': 'Description', 'data': self.description})
        # attributes.append({'title': 'Area', 'data': '%s sq miles' %format_precision(self.area_in_sq_miles, 2)})
        self.summary_reports(attributes)
        return { 'event': 'click', 'attributes': attributes }
    
    @classmethod
    def fill_color(self):
        return '776BAEFD'      
    
    @classmethod
    def outline_color(self):
        return '776BAEFD'    

    def clip_to_grid(self): 
        geom = self.geometry_orig
        clipped_shape = clip_to_grid(geom)
        if clipped_shape:
            return LargestPolyFromMulti(clipped_shape)
        else:
            return clipped_shape

    def save(self, *args, **kwargs):
        self.geometry_final = self.clip_to_grid()
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
