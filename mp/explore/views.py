# Create your views here.
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from data_manager.models import *
from utils import get_domain
import os
import settings


def data_catalog(request, project=None, template='catalog.html'):
    from mp_settings.models import MarinePlannerSettings
    try:
        if project:
            activeSettings = MarinePlannerSettings.objects.get(slug_name=project)
        else:
            activeSettings = MarinePlannerSettings.objects.get(active=True)
        
        project_name = activeSettings.project_name 
        
        project_logo = activeSettings.project_logo 
        # try:
        #     if project_logo:
        #         url_validator = URLValidator(verify_exists=False)
        #         url_validator(project_logo)
        # except ValidationError, e:
        #     project_logo = os.path.join(settings.MEDIA_URL, project_logo) 
            
        project_icon = activeSettings.project_icon 
        # try:
        #     url_validator = URLValidator(verify_exists=False)
        #     url_validator(project_icon)
        # except ValidationError, e:
        #     project_icon = os.path.join(settings.MEDIA_URL, project_icon)  
            
        project_home_page = activeSettings.project_home_page 
        
        try:
            themes = activeSettings.table_of_contents.themes.all().order_by('display_name')
            themes_with_layers = getTOCThemesAndLayers(themes)
        except:
            themes = Theme.objects.all().order_by('display_name')
            themes_with_layers = add_learn_links(themes)
            add_ordered_layers_lists(themes_with_layers)
        context = {'MEDIA_URL': settings.MEDIA_URL, 'themes': themes_with_layers, 'project_name': project_name, 'project_logo': project_logo, 'project_icon': project_icon, 'project_home_page': project_home_page, 'domain': get_domain(8000), 'domain8010': get_domain()}
        return render_to_response(template, RequestContext(request, context)) 
    except:
        themes = Theme.objects.all().order_by('display_name')
        themes_with_links = add_learn_links(themes)
        add_ordered_layers_lists(themes_with_links)
        context = {'MEDIA_URL': settings.MEDIA_URL, 'themes': themes_with_links, 'domain': get_domain(8000), 'domain8010': get_domain()}
        return render_to_response(template, RequestContext(request, context)) 

def data_needs(request, template='needs.html'):
    themes = Theme.objects.all().order_by('display_name')
    ordered_themes, theme_dict = add_ordered_needs_lists(themes)
    context = {'themes': themes, 'theme_dict': theme_dict, 'ordered_themes': ordered_themes, 'domain': get_domain(8000), 'domain8010': get_domain()}
    return render_to_response(template, RequestContext(request, context)) 
    
def add_ordered_needs_lists(themes_list):
    theme_dict = {}
    ordered_themes = []
    for theme in themes_list:
        needs = theme.dataneed_set.all().exclude(archived=True).order_by('name')
        if len(needs) > 0:
            ordered_themes.append(theme)
            theme_dict[theme] = needs
    return ordered_themes, theme_dict
    
def getTOCThemesAndLayers(themes):
    themes_list = []
    for theme in themes:
        num_layers = len([layer.name for layer in theme.layers.all() if not layer.is_parent and not layer.layer_type == 'placeholder'])
        ordered_layers = theme.layers.all().exclude(layer_type='placeholder').order_by('name')
        themes_list.append({'theme': theme, 'num_layers': num_layers, 'layers': ordered_layers})    
    return themes_list
    
def add_ordered_layers_lists(themes_list): 
    for theme_dict in themes_list:
        layers = theme_dict['theme'].layer_set.all().exclude(layer_type='placeholder').order_by('name')
        theme_dict['layers'] = layers
    
def add_learn_links(themes):
    theme_dict = []
    for theme in themes:
        num_layers = len([layer.name for layer in theme.layer_set.all() if not layer.is_parent and not layer.layer_type == 'placeholder'])
        theme_dict.append({'theme': theme, 'num_layers': num_layers, 'learn_link': theme.learn_link})
    return theme_dict
    
def tiles_page(request, slug=None, template='tiles_page.html'):
    layer = get_object_or_404(Layer, slug_name=slug)
    orig_url = layer.url
    arctile_url = orig_url.replace('{z}', '{level}').replace('{x}', '{col}').replace('{y}', '{row}')
    arcrest_url = orig_url.replace('/export', '')
    context = {'layer': layer, 'arctile_url': arctile_url, 'arcrest_url': arcrest_url, 'domain': get_domain(8000)}
    return render_to_response(template, RequestContext(request, context)) 

def map_tile_example(request, slug=None, template='map_tile_example.html'):
    map_settings = getMapSettings()
    layer = get_object_or_404(Layer, slug_name=slug)
    print map_settings
    context = {'layer': layer, 'MEDIA_URL': settings.MEDIA_URL, 'map_settings': map_settings}
    return render_to_response(template, RequestContext(request, context)) 

def map_tile_esri_example(request, slug=None, template='map_tile_esri_example.html'):
    map_settings = getMapSettings()
    layer = get_object_or_404(Layer, slug_name=slug)
    orig_url = layer.url
    arctile_url = orig_url.replace('{z}', '{level}').replace('{x}', '{col}').replace('{y}', '{row}')
    context = {'layer': layer, 'arctile_url': arctile_url, 'map_settings': map_settings}
    return render_to_response(template, RequestContext(request, context)) 

def map_tile_leaflet_example(request, slug=None, template='map_tile_leaflet_example.html'):
    map_settings = getMapSettings()
    layer = get_object_or_404(Layer, slug_name=slug)
    orig_url = layer.url
    leaflet_url = orig_url.replace('$', '')
    context = {'layer': layer, 'leaflet_url': leaflet_url, 'map_settings': map_settings}
    return render_to_response(template, RequestContext(request, context)) 

def arcrest_example(request, slug=None, template='arcrest_example.html'):
    map_settings = getMapSettings()
    layer = get_object_or_404(Layer, slug_name=slug)
    context = {'layer': layer, 'map_settings': map_settings}
    return render_to_response(template, RequestContext(request, context)) 

def linkify(text):
    return text.lower().replace(' ', '-')

def getMapSettings(): 
    from mp_settings.models import MarinePlannerSettings
    import json
    try:
        activeSettings = MarinePlannerSettings.objects.get(active=True)        
        latitude = activeSettings.latitude        
        longitude = activeSettings.longitude 
        zoom = activeSettings.zoom
        return json.dumps({'lat': latitude, 'lng': longitude, 'zoom': zoom})
    except:
        return json.dumps({})
    
