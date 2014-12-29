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
    
    # Depth Range (meters, avg: 350m - 0m)
    # Boolean field is the anchor, and used as the base name for rendering the form. 
    # - Help_text on the boolean is included in the popup text "info" icon.
    # - Label is used as the icon label 
    # bathy_avg = forms.BooleanField(label="Average Depth", required=False, help_text="Ocean depth in meters", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # bathy_avg_min = forms.FloatField(required=False, initial=10, widget=forms.TextInput(attrs={'class':'slidervalue'}))
    # bathy_avg_max = forms.FloatField(required=False, initial=50, widget=TextInputWithUnit(attrs={'class':'slidervalue'}))
    # bathy_avg_input = forms.FloatField(widget=DualSliderWidget('bathy_avg_min', 'bathy_avg_max', min=1, max=300, step=1))

    inlet_distance = forms.BooleanField(label="Distance to Coastal Inlet", required=False, help_text="Maximum distance to Nearest Inlet", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    inlet_distance_max = forms.FloatField(required=False, initial=15, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=15000, step=1000))

    shore_distance = forms.BooleanField(label="Distance to Shore", required=False, help_text="Distance to Shore", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    shore_distance_min = forms.FloatField(required=False, initial=2000, widget=forms.TextInput(attrs={'class':'slidervalue'}))
    # shore_distance_max = forms.FloatField(required=False, initial=10000, widget=TextInputWithUnit(attrs={'class':'slidervalue'}, unit='meters'))
    shore_distance_max = forms.FloatField(required=False, initial=10000, widget=forms.TextInput(attrs={'class':'slidervalue'}))
    shore_distance_input = forms.FloatField(widget=DualSliderWidget('shore_distance_min', 'shore_distance_max', min=0, max=12000, step=1000))

    fish_abundance = forms.BooleanField(label="Fish Abundance", required=False, help_text="Fish Abundance", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    fish_abundance_max = forms.FloatField(required=False, initial=50, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=500, step=10))

    fish_richness = forms.BooleanField(label="Fish Richness", required=False, help_text="Fish Richness", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    fish_richness_max = forms.FloatField(required=False, initial=15, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=50, step=5))

    coral_richness = forms.BooleanField(label="Coral Richness", required=False, help_text="Coral Richness", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_richness_max = forms.FloatField(required=False, initial=5, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=25, step=1))

    coral_density = forms.BooleanField(label="Coral Density", required=False, help_text="Coral Density", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_density_max = forms.FloatField(required=False, initial=1, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=3, step=1))

    coral_size = forms.BooleanField(label="Coral Size", required=False, help_text="Coral Size", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_size_max = forms.FloatField(required=False, initial=10, widget=SliderWidget(attrs={'class':'slidervalue'}, min=0, max=500, step=10))
    
    # coral_p = forms.BooleanField(label="Corals", required=False, help_text="Coral cover", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # mangrove_p = forms.BooleanField(label="Mangroves", required=False, help_text="Mangrove cover", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    
    
    def get_step_1_fields(self):
        """Defines the fields that we want to show on the form in step 1, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('inlet_distance', None, 'inlet_distance_max'), 
                ('shore_distance', 'shore_distance_min', 'shore_distance_max', 'shore_distance_input'))

        return self._get_fields(names)

    
    def get_step_2_fields(self):
        """Defines the fields that we want to show on the form in step 2, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('fish_abundance', None, 'fish_abundance_max'),
                ('fish_richness', None, 'fish_richness_max'),
                ('coral_density', None, 'coral_density_max'),
                ('coral_richness', None, 'coral_richness_max'),
                ('coral_size', None, 'coral_size_max'))
        
        return self._get_fields(names)

    def get_steps(self):
        return self.get_step_1_fields(), self.get_step_2_fields()

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

