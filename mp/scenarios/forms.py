# coding: utf-8
from madrona.features.forms import FeatureForm, SpatialFeatureForm
from django import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from django.forms.widgets import *
from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import fromstr
from os.path import splitext, split
from madrona.analysistools.widgets import SliderWidget, DualSliderWidget
from models import *
from widgets import AdminFileWidget, SliderWidgetWithTooltip, DualSliderWidgetWithTooltip, CheckboxSelectMultipleWithTooltip, CheckboxSelectMultipleWithObjTooltip 

# http://www.neverfriday.com/sweetfriday/2008/09/-a-long-time-ago.html
class FileValidationError(forms.ValidationError):
    def __init__(self):
        super(FileValidationError, self).__init__('Document types accepted: ' + ', '.join(ValidFileField.valid_file_extensions))
        
class ValidFileField(forms.FileField):
    """A validating document upload field"""
    valid_file_extensions = ['odt', 'pdf', 'doc', 'xls', 'txt', 'csv', 'kml', 'kmz', 'jpeg', 'jpg', 'png', 'gif', 'zip']

    def __init__(self, *args, **kwargs):
        super(ValidFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        f = super(ValidFileField, self).clean(data, initial)
        if f:
            ext = splitext(f.name)[1][1:].lower()
            if ext in ValidFileField.valid_file_extensions: 
                # check data['content-type'] ?
                return f
            raise FileValidationError()


class InputWithUnit(Input):
    """Modified Input class that accepts a "unit" parameter, and stores the 
    value in the unit attribute. 
    This is allows additional data associated with a field to be exposed to the 
    template renderer. Later improvements would be to stick this value on the 
    field itself rather than the widget. Also, make it a dictionary rather than
    a single value, so other arbitrary values can be brough forward.   
    """
    def __init__(self, attrs=None, unit=None):
        super(InputWithUnit, self).__init__(attrs)
        self.unit = str(unit)

class TextInputWithUnit(forms.TextInput, InputWithUnit):
    pass

class ScenarioForm(FeatureForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), required=False)
    
    shore_distance = forms.BooleanField(label="Distance to Shore", required=False, help_text="Distance to Shore", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    shore_distance_min = forms.FloatField(required=False, initial=3000, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters'}))
    shore_distance_max = forms.FloatField(required=False, initial=10000, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    # shore_distance_max = forms.FloatField(required=False, initial=10000, widget=TextInputWithUnit(attrs={'class':'slidervalue'}, unit='meters'))
    shore_distance_input = forms.FloatField(widget=DualSliderWidget('shore_distance_min', 'shore_distance_max', min=0, max=13000, step=1000))

    pier_distance = forms.BooleanField(label="Distance to Pier", required=False, help_text="Distance to Nearest Pier", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    pier_distance_min = forms.FloatField(required=False, initial=5000, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters'}))
    pier_distance_max = forms.FloatField(required=False, initial=20000, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    pier_distance_input = forms.FloatField(widget=DualSliderWidget('pier_distance_min', 'pier_distance_max', min=0, max=35000, step=1000))

    inlet_distance = forms.BooleanField(label="Distance to Coastal Inlet", required=False, help_text="Minimum distance to Nearest Inlet", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    inlet_distance_min = forms.FloatField(required=False, initial=3000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters', 'post_text': 'meters'}, min=0, max=16000, step=1000))

    outfall_distance = forms.BooleanField(label="Distance to Outfall", required=False, help_text="Minimum distance to Nearest Outfall", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    outfall_distance_min = forms.FloatField(required=False, initial=3000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters', 'post_text': 'meters'}, min=0, max=10000, step=1000))

    # Depth Range (meters, avg: 0m - 212m)
    # Boolean field is the anchor, and used as the base name for rendering the form. 
    # - Help_text on the boolean is included in the popup text "info" icon.
    # - Label is used as the icon label 
    depth = forms.BooleanField(label="Average Depth", required=False, help_text="Ocean depth in meters", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # depth_min = forms.FloatField(required=False, initial=10, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters', 'post_text': 'meters'}, min=1, max=220, step=1))
    depth_min = forms.FloatField(required=False, initial=10, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters'}))
    depth_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    depth_input = forms.FloatField(widget=DualSliderWidget('depth_min', 'depth_max', min=1, max=220, step=1))

    # acropora_pa = forms.BooleanField(label="Acropora Presence / Absence", required=False, help_text="Select cells based on Presence or Absence", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # acropora_pa_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('A', 'Absence'), ('P', 'Presence')), initial='A')
    # Giving up on RadioSelect, it refused to return anything other than the last choice as the selection to the server...Select widget seems to work fine through...

    injury_site = forms.BooleanField(label="Injury Site Yes/No", required=False, help_text="Whether a cell contains at least one recorded grounding or anchoring event in the DEP database", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    injury_site_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters', 'layer_id': '918', 'layer_title': 'Reef Injury Site'}), choices=(('Y', 'Yes'), ('N', 'No')), initial='Y')

    large_live_coral = forms.BooleanField(label="Large Live Coral Yes/No", required=False, help_text="Whether a cell contains at least one known live coral greater than 2 meters in width", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    large_live_coral_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('Y', 'Yes'), ('N', 'No')), initial='Y')

    acerv_area = forms.BooleanField(label="Area of Dense Acropora C.", required=False, help_text="Area of mapped Dense Acropora cervicornis patches in m²", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    acerv_area_min = forms.FloatField(required=False, initial=1000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Area in meters sq', 'post_text': 'meters'}, min=0, max=10000, step=500))

    reef_area = forms.BooleanField(label="Area of Coral Reef", required=False, help_text="Area of Coral Reef and Colonized hardbottom habitats in m²", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    reef_area_min = forms.FloatField(required=False, initial=1000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Area in meters sq', 'post_text': 'meters'}, min=0, max=4000, step=100))

    sg_area = forms.BooleanField(label="Area of Seagrass", required=False, help_text="Area of Seagrass habitats in m²", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': "318", 'layer_title': "Show Seagrass Habitats"}))
    sg_area_min = forms.FloatField(required=False, initial=1000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Area in meters sq', 'post_text': 'meters'}, min=0, max=4000, step=100))

    sand_area = forms.BooleanField(label="Area of Sand Habitat", required=False, help_text="Area of Sand habitat in m²", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    sand_area_min = forms.FloatField(required=False, initial=1000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Area in meters sq', 'post_text': 'meters'}, min=0, max=4000, step=100))

    art_area = forms.BooleanField(label="Area of Artificial Habitats", required=False, help_text="Area of Artificial habitats (Sand borrow areas, artificial reefs, inlets , jettys, channels,) in m²", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    art_area_min = forms.FloatField(required=False, initial=1000, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Area in meters sq', 'post_text': 'meters'}, min=0, max=4000, step=100))

    fish_richness = forms.BooleanField(label="Fish Richness", required=False, help_text="Estimated # of species per survey area", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    fish_richness_max = forms.FloatField(required=False, initial=15, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=40, step=5))

    coral_richness = forms.BooleanField(label="Coral Richness", required=False, help_text="Estimated # of species per survey area", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_richness_max = forms.FloatField(required=False, initial=15, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=40, step=5))

    coral_density = forms.BooleanField(label="Coral Density", required=False, help_text="Estimated # of organisms per sq meter", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_density_max = forms.FloatField(required=False, initial=2, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=5, step=1))

    coral_size = forms.BooleanField(label="Coral Size", required=False, help_text="Coral Size", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_size_max = forms.FloatField(required=False, initial=50, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=500, step=10))
    
    # coral_p = forms.BooleanField(label="Corals", required=False, help_text="Coral cover", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # mangrove_p = forms.BooleanField(label="Mangroves", required=False, help_text="Mangrove cover", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    
    '''
    Depth and Distances
    '''
    def get_step_1_fields(self):
        """Defines the fields that we want to show on the form in step 1, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('depth', 'depth_min', 'depth_max', 'depth_input'),
                ('shore_distance', 'shore_distance_min', 'shore_distance_max', 'shore_distance_input'),
                ('pier_distance', 'pier_distance_min', 'pier_distance_max', 'pier_distance_input'),
                ('inlet_distance', 'inlet_distance_min', None), 
                ('outfall_distance', 'outfall_distance_min', None)) 

        return self._get_fields(names)

    '''
    Fish and Coral
    '''
    def get_step_2_fields(self):
        """Defines the fields that we want to show on the form in step 2, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('fish_richness', None, 'fish_richness_max'),
                # ('acropora_pa', None, None, 'acropora_pa_input'), 
                ('acerv_area', 'acerv_area_min', None), 
                ('reef_area', 'reef_area_min', None), 
                ('coral_density', None, 'coral_density_max'),
                ('coral_richness', None, 'coral_richness_max'),
                ('coral_size', None, 'coral_size_max'),
                ('large_live_coral', None, None, 'large_live_coral_input'))
        
        return self._get_fields(names)

    '''
    Other Habitats
    '''
    def get_step_3_fields(self):
        """Defines the fields that we want to show on the form in step 2, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('injury_site', None, None, 'injury_site_input'), 
                ('sg_area', 'sg_area_min', None), 
                ('sand_area', 'sand_area_min', None), 
                ('art_area', 'art_area_min', None))
        
        return self._get_fields(names)

    def get_steps(self):
        return self.get_step_1_fields(), self.get_step_2_fields(), self.get_step_3_fields()

    def _get_fields(self, names):
        fields = []
        for name_list in names: 
            group = []
            for name in name_list: 
                if name:
                    group.append(self[name])
                else:
                    group.append(None)
            fields.append(group)
        return fields

      
    def save(self, commit=True):
        inst = super(FeatureForm, self).save(commit=False)
        if self.data.get('clear_support_file'):
            inst.support_file = None
        if commit:
            inst.save()
        return inst
    
    class Meta(FeatureForm.Meta):
        model = Scenario
        exclude = list(FeatureForm.Meta.exclude)
        for f in model.output_fields():
            exclude.append(f.attname)
        
        widgets = {
            
        }

