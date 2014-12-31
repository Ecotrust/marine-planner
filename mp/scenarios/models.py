# coding: utf-8

import os
import time
import json
from picklefield import PickledObjectField
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.html import escape
from madrona.common.utils import asKml
from madrona.common.jsonutils import get_properties_json, get_feature_json
from madrona.features import register
from madrona.analysistools.models import Analysis
from general.utils import miles_to_meters, feet_to_meters, meters_to_feet, mph_to_mps, mps_to_mph, format
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.db.models.aggregates import Union

@register
class Scenario(Analysis):
    # depth = models.BooleanField()
    # depth_avg = models.IntegerField(null=True, blank=True)
    # depth_min = models.IntegerField(null=True, blank=True)
    # depth_max = models.IntegerField(null=True, blank=True)

    # rugosity = models.BooleanField()
    # rugosity_avg = models.IntegerField(null=True, blank=True)
    # rugosity_min = models.IntegerField(null=True, blank=True)
    # rugosity_max = models.IntegerField(null=True, blank=True)

    # slope = models.BooleanField()
    # slope_avg = models.IntegerField(null=True, blank=True)
    # slope_min = models.IntegerField(null=True, blank=True)
    # slope_max = models.IntegerField(null=True, blank=True)

    region = models.TextField(null=True, blank=True)
    county = models.TextField(null=True, blank=True)

    habitat = models.TextField(null=True, blank=True)
    modifier = models.TextField(null=True, blank=True)
    type_1 = models.TextField(null=True, blank=True)
    type_2 = models.TextField(null=True, blank=True)

    fish_abundance = models.BooleanField()
    fish_abundance_min = models.FloatField(null=True, blank=True)
    fish_abundance_max = models.FloatField(null=True, blank=True)

    fish_richness = models.BooleanField()
    fish_richness_min = models.FloatField(null=True, blank=True)
    fish_richness_max = models.FloatField(null=True, blank=True)

    coral_richness = models.BooleanField()
    coral_richness_min = models.FloatField(null=True, blank=True)
    coral_richness_max = models.FloatField(null=True, blank=True)

    coral_density = models.BooleanField()
    coral_density_min = models.FloatField(null=True, blank=True)
    coral_density_max = models.FloatField(null=True, blank=True)

    coral_size = models.BooleanField()
    coral_size_min = models.FloatField(null=True, blank=True)
    coral_size_max = models.FloatField(null=True, blank=True)

    inlet_distance = models.BooleanField()
    inlet_distance_min = models.FloatField(null=True, blank=True)
    inlet_distance_max = models.FloatField(null=True, blank=True)

    shore_distance = models.BooleanField()
    shore_distance_min = models.FloatField(null=True, blank=True)
    shore_distance_max = models.FloatField(null=True, blank=True)

    prev_impact = models.TextField(null=True, blank=True)
    acropora_pa = models.TextField(null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    satisfied = models.BooleanField(default=True, help_text="Am I satisfied?")
    active = models.BooleanField(default=True)
            
    grid_cells = models.TextField(verbose_name='Grid Cell IDs', null=True, blank=True)
    geometry_final_area = models.FloatField(verbose_name='Total Area', null=True, blank=True)
    geometry_dissolved = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Filter result dissolved")
                
    @property
    def serialize_attributes(self):
        """
        Return attributes in text format. Used to display information on click in the planner. 
        """
        from general.utils import format
        attributes = []

        if self.inlet_distance:
        	attributes.append({ 'title': 'Maximum Distance to Coastal Inlet',
        						'data':  str(int(self.inlet_distance_max)/1000) + ' km'})

        if self.shore_distance:
        	attributes.append({ 'title': 'Distance to Shore',
        						'data':  str(int(self.shore_distance_min)/1000) + ' to ' + str(int(self.shore_distance_max)/1000) + ' km'})

        if self.fish_abundance: 
        	attributes.append({ 'title': 'Maximum Fish Abundance',
        						'data':  str(int(self.fish_abundance_max)) + ' units'})

        if self.fish_richness: 
        	attributes.append({ 'title': 'Maximum Fish Richness',
        						'data':  str(int(self.fish_richness_max)) + ' units'})

        if self.coral_density: 
        	attributes.append({ 'title': 'Maximum Coral Density',
        						'data':  str(int(self.coral_density_max)) + ' units'})

        if self.coral_richness: 
        	attributes.append({ 'title': 'Maximum Coral Richness',
        						'data':  str(int(self.coral_richness_max)) + ' units'})

        if self.coral_size: 
        	attributes.append({ 'title': 'Maximum Coral Size',
        						'data':  str(int(self.coral_size_max)) + ' units'})

        # if self.coral_p or self.subveg_p or self.protarea_p:
        #     exclusions = ''
        #     if self.coral_p:
        #         exclusions += '<br>&nbsp;&nbsp; Corals'
        #     if self.subveg_p:
        #         exclusions += '<br>&nbsp;&nbsp; Submerged Vegetation'
        #     if self.protarea_p:
        #         exclusions += '<br>&nbsp;&nbsp; Protected Areas'

        #     attributes.append(dict(title='Areas containing the following were excluded', data=exclusions))        

        attributes.append({'title': 'Number of Grid Cells', 
                           'data': '{:,}'.format(self.grid_cells.count(',')+1)})
        return { 'event': 'click', 'attributes': attributes }
    
    
    def geojson(self, srid):
        props = get_properties_json(self)
        props['absolute_url'] = self.get_absolute_url()
        json_geom = self.geometry_dissolved.transform(srid, clone=True).json
        return get_feature_json(json_geom, json.dumps(props))
    
    def run(self):
        query = GridCell.objects.all()
        
        # TODO: This would be nicer if it generically knew how to filter fields
        # by name, and what kinds of filters they were. For now, hard code. 
        
        # if self.bathy_avg:
        #     query = query.filter(bathy_avg__range=(self.bathy_avg_min, 
        #                                            self.bathy_avg_max))
        
        if self.inlet_distance:
            query = query.filter(inlet_distance__gte=self.inlet_distance_max)
        
        if self.shore_distance:
            query = query.filter(shore_distance__range=(self.shore_distance_min, self.shore_distance_max))

        if self.fish_abundance:
            query = query.filter(fish_abundance__gte=self.fish_abundance_max)
        
        if self.fish_richness:
            query = query.filter(fish_richness__gte=self.fish_richness_max)

        if self.coral_richness:
            query = query.filter(coral_richness__gte=self.coral_richness_max)
        
        if self.coral_density:
            query = query.filter(coral_density__gte=self.coral_density_max)
        
        if self.coral_size:
            query = query.filter(coral_size__gte=self.coral_size_max)
        
        # if self.mangrove_p:
        #     query = query.filter(mangrove_p=0)
        
        if len(query) == 0:
        	self.satisfied = False;
        	# raise Exception("No lease blocks available with the current filters.")       

        dissolved_geom = query.aggregate(Union('geometry'))        
        if dissolved_geom['geometry__union']:
            dissolved_geom = dissolved_geom['geometry__union']
        else:
            raise Exception("No lease blocks available with the current filters.")
        
        if type(dissolved_geom) == MultiPolygon:
            self.geometry_dissolved = dissolved_geom
        else:
            self.geometry_dissolved = MultiPolygon(dissolved_geom, srid=dissolved_geom.srid)
        self.active = True
        
        import datetime;start=datetime.datetime.now()
        self.geometry_final_area = self.geometry_dissolved.area
        
        self.grid_cells = ','.join(str(i) 
                                     for i in query.values_list('id', flat=True))
        
        print("Elapsed:", datetime.datetime.now() - start)
               
        if self.grid_cells == '':
            self.satisfied = False
        else:
            self.satisfied = True
        return True        
    
    def save(self, rerun=None, *args, **kwargs):
        if rerun is None and self.pk is None:
            rerun = True
        if rerun is None and self.pk is not None: #if editing a scenario and no value for rerun is given
            rerun = False
            if not rerun:
                orig = Scenario.objects.get(pk=self.pk)
                #TODO: keeping this in here til I figure out why self.grid_cells and self.geometry_final_area are emptied when run() is not called
                rerun = True
                if not rerun:
                    for f in Scenario.input_fields():
                        # Is original value different from form value?
                        if getattr(orig, f.name) != getattr(self, f.name):
                            #print 'input_field, %s, has changed' %f.name
                            rerun = True
                            break                                                                                                                   
                if not rerun:
                    '''
                        the substrates need to be grabbed, then saved, then grabbed again because 
                        both getattr calls (orig and self) return the same original list until the model has been saved 
                        (perhaps because form.save_m2m has to be called), after which calls to getattr will 
                        return the same list (regardless of whether we use orig or self)
                    ''' 
                    orig_weas = set(getattr(self, 'input_wea').all())   
                    orig_substrates = set(getattr(self, 'input_substrate').all())  
                    orig_sediments = set(getattr(self, 'input_sediment').all())                    
                    super(Scenario, self).save(rerun=False, *args, **kwargs)  
                    new_weas = set(getattr(self, 'input_wea').all())                   
                    new_substrates = set(getattr(self, 'input_substrate').all()) 
                    new_sediments = set(getattr(self, 'input_sediment').all())   
                    if orig_substrates != new_substrates or orig_sediments != new_sediments or orig_weas != new_weas:
                        rerun = True    
            super(Scenario, self).save(rerun=rerun, *args, **kwargs)
        else: #editing a scenario and rerun is provided 
            super(Scenario, self).save(rerun=rerun, *args, **kwargs)    
    
    def __unicode__(self):
        return u'%s' % self.name
        
    def support_filename(self):
        return os.path.basename(self.support_file.name)
        
    @classmethod
    def mapnik_geomfield(self):
        return "output_geom"

    @classmethod
    def mapnik_style(self):
        import mapnik
        polygon_style = mapnik.Style()
        
        ps = mapnik.PolygonSymbolizer(mapnik.Color('#ffffff'))
        ps.fill_opacity = 0.5
        
        ls = mapnik.LineSymbolizer(mapnik.Color('#555555'),0.75)
        ls.stroke_opacity = 0.5
        
        r = mapnik.Rule()
        r.symbols.append(ps)
        r.symbols.append(ls)
        polygon_style.rules.append(r)
        return polygon_style     
    
    @classmethod
    def input_parameter_fields(klass):
        return [f for f in klass._meta.fields if f.attname.startswith('input_parameter_')]

    @classmethod
    def input_filter_fields(klass):
        return [f for f in klass._meta.fields if f.attname.startswith('input_filter_')]

    @property
    def grid_cells_set(self):
        if len(self.grid_cells) == 0:  #empty result
            gridcell_ids = []
        else:
            gridcell_ids = [int(id) for id in self.grid_cells.split(',')]
        gridcells = GridCell.objects.filter(pk__in=gridcell_ids)
        return gridcells
    
    @property
    def num_lease_blocks(self):
        if self.grid_cells == '':
            return 0
        return len(self.grid_cells.split(','))
    
    @property
    def geometry_is_empty(self):
        return len(self.grid_cells) == 0
    
    @property
    def input_wea_names(self):
        return [wea.wea_name for wea in self.input_wea.all()]
        
    @property
    def input_substrate_names(self):
        return [substrate.substrate_name for substrate in self.input_substrate.all()]
        
    @property
    def input_sediment_names(self):
        return [sediment.sediment_name for sediment in self.input_sediment.all()]
    
    #TODO: is this being used...?  Yes, see show.html
    @property
    def has_wind_energy_criteria(self):
        wind_parameters = Scenario.input_parameter_fields()
        for wp in wind_parameters:
            if getattr(self, wp.name):
                return True
        return False
        
    @property
    def has_shipping_filters(self):
        shipping_filters = Scenario.input_filter_fields()
        for sf in shipping_filters:
            if getattr(self, sf.name):
                return True
        return False 
        
    @property
    def has_military_filters(self):
        return False
    
    @property
    def color(self):
        try:
            return Objective.objects.get(pk=self.input_objectives.values_list()[0][0]).color
        except:
            return '778B1A55'                    
        
    @property
    def get_id(self):
        return self.id
    
    class Options:
        verbose_name = 'Spatial Design for Wind Energy'
        icon_url = 'marco/img/multi.png'
        form = 'scenarios.forms.ScenarioForm'
        form_template = 'scenario/form.html'
        show_template = 'scenario/show.html'

#no longer needed?
# class Objective(models.Model):
#     name = models.CharField(max_length=35)
#     color = models.CharField(max_length=8, default='778B1A55')
    
#     def __unicode__(self):
#         return u'%s' % self.name        

#no longer needed?
# class Parameter(models.Model):
#     ordering_id = models.IntegerField(null=True, blank=True)
#     name = models.CharField(max_length=35, null=True, blank=True)
#     shortname = models.CharField(max_length=35, null=True, blank=True)
#     objectives = models.ManyToManyField("Objective", null=True, blank=True)
    
#     def __unicode__(self):
#         return u'%s' % self.name

class GridCell(models.Model):
    # depth_avg = models.IntegerField(null=True, blank=True)
    # depth_min = models.IntegerField(null=True, blank=True)
    # depth_max = models.IntegerField(null=True, blank=True)
    # rugosity_avg = models.IntegerField(null=True, blank=True)
    # rugosity_min = models.IntegerField(null=True, blank=True)
    # rugosity_max = models.IntegerField(null=True, blank=True)
    # slope_avg = models.IntegerField(null=True, blank=True)
    # slope_min = models.IntegerField(null=True, blank=True)
    # slope_max = models.IntegerField(null=True, blank=True)
    
    region = models.TextField(null=True, blank=True)
    county = models.TextField(null=True, blank=True)

    habitat = models.TextField(null=True, blank=True)
    modifier = models.TextField(null=True, blank=True)
    type_1 = models.TextField(null=True, blank=True)
    type_2 = models.TextField(null=True, blank=True)
    
    fish_abundance = models.IntegerField(null=True, blank=True)
    fish_richness = models.IntegerField(null=True, blank=True)
    coral_richness = models.IntegerField(null=True, blank=True)
    coral_density = models.IntegerField(null=True, blank=True)
    coral_size = models.IntegerField(null=True, blank=True)
    
    inlet_distance = models.IntegerField(null=True, blank=True)
    shore_distance = models.IntegerField(null=True, blank=True)
    
    prev_impact = models.TextField(null=True, blank=True)
    acropora_pa = models.TextField(null=True, blank=True)
    
    centroid = models.PointField(null=True, blank=True)

    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, 
                                    null=True, blank=True, 
                                    verbose_name="Grid Cell Geometry")
    objects = models.GeoManager()

