# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.cache import cache_page
from models import *


#@cache_page(60 * 60 * 24, key_prefix="data_manager_get_json")
def get_json(request, project=None):
    from mp_settings.models import *
    try:
        if project:
            activeSettings = MarinePlannerSettings.objects.get(slug_name=project)
        else:
            activeSettings = MarinePlannerSettings.objects.get(active=True)
        #if activeSettings.table_of_contents is not None:
        layer_list = []
        for theme in activeSettings.table_of_contents.themes.all():
            for layer in theme.layers.all().order_by('name'):
                layer_list.append(layer.toDict)
        json = {
            "state": { "activeLayers": [] },
            "layers": layer_list,
            "themes": [theme.toDict for theme in activeSettings.table_of_contents.themes.all().order_by('display_name')],
            "success": True
        }
        return HttpResponse(simplejson.dumps(json))
    except:
        pass
    json = {
        "state": { "activeLayers": [] },
        "layers": [layer.toDict for layer in Layer.objects.filter(is_sublayer=False).exclude(layer_type='placeholder').order_by('name')],
        "themes": [theme.toDict for theme in Theme.objects.all().order_by('display_name')],
        "success": True
    }
    return HttpResponse(simplejson.dumps(json))


def create_layer(request):
    if request.POST:
        try:
            url, name, type, themes = get_layer_components(request.POST)
            layer = Layer(
                url = url,
                name = name,
                layer_type = type
            )
            layer.save()
            
            for theme_id in themes:
                theme = Theme.objects.get(id=theme_id)
                layer.themes.add(theme)
            layer.save()
            
        except Exception, e:
            return HttpResponse(e.message, status=500)

        result = layer_result(layer, message="Saved Successfully")            
        return HttpResponse(simplejson.dumps(result))

    
def update_layer(request, layer_id):
    if request.POST:
        layer = get_object_or_404(Layer, id=layer_id)
        
        try:
            url, name, type, themes = get_layer_components(request.POST)
            layer.url = url
            layer.name = name        
            layer.save()
            
            for theme in layer.themes.all():
                layer.themes.remove(theme)
            for theme_id in themes:
                theme = Theme.objects.get(id=theme_id)
                layer.themes.add(theme)            
            layer.save()  
            
        except Exception, e:
            return HttpResponse(e.message, status=500)

        result = layer_result(layer, message="Edited Successfully")
        return HttpResponse(simplejson.dumps(result))
    
    
def get_layer_components(request_dict, url='', name='', type='XYZ', themes=[]):
    if 'url' in request_dict:
        url = request_dict['url']
    if 'name' in request_dict:
        name = request_dict['name']
    if 'type' in request_dict:
        type = request_dict['type']
    if 'themes' in request_dict:
        themes = request_dict.getlist('themes') 
    return url, name, type, themes
    
    
def layer_result(layer, status_code=1, success=True, message="Success"):
    result = {
        "status_code":status_code,  
        "success":success, 
        "message":message,
        "layer": layer.toDict,
        "themes": [theme.id for theme in layer.themes.all()]
    }
    return result

def load_config(request): 
    import json
    import os
    from django.core.exceptions import ObjectDoesNotExist
    from django.template.defaultfilters import slugify

    json_data = open('data_manager/fixtures/wa_config.json')
    wa_config = json.load(json_data)
    toc_obj = wa_config['Themes'][0]['Marine Spatial Planning']['TOC'][0]
    layers = wa_config['layersNew']
    base_url = wa_config['DNRAGSServiceURL']
   
    try:
        toc = TOC.objects.get(name='WA_CMSP')
    except ObjectDoesNotExist:
        toc = TOC(name='WA_CMSP')
        toc.save()
    for layer_name, layer_obj in layers.iteritems():
        if 'url' in layer_obj and layer_obj['url'] != "":
            relative_url = layer_obj['url'].replace('DNRAGSServiceURL/','')
            absolute_url = os.path.join(base_url, relative_url, 'export')
            try:
                layer = Layer.objects.get(name=layer_name)
            except ObjectDoesNotExist:
                layer = Layer(name=layer_name, layer_type='ArcRest', url=absolute_url, arcgis_layers='0')
                layer.save()
    
    for theme_name, layer_list in toc_obj.iteritems():
        try:
            theme = TOCTheme.objects.get(display_name=theme_name)
        except ObjectDoesNotExist:
            theme = TOCTheme(display_name=theme_name, name=slugify(theme_name))
            theme.save()
        for layer_obj in layer_list:
            try:
                layer = Layer.objects.get(name=layer_obj['layerID'])
                theme.layers.add(layer)
            except ObjectDoesNotExist:
                pass
        theme.save()
        toc.themes.add(theme)
    return HttpResponse('layers and themes successfully loaded into WA_CMSP TOC object', status=200)
