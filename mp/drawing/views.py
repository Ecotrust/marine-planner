from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry
from madrona.features.models import Feature
from madrona.features import get_feature_by_uid
from madrona.common.utils import LargestPolyFromMulti
from scenarios.models import GridCell
from models import *
from ofr_manipulators import clip_to_grid
from simplejson import dumps
    


'''
'''
def get_drawings(request):
    json = []
    
    drawings = AOI.objects.filter(user=request.user).order_by('date_created')
    for drawing in drawings:
        sharing_groups = [group.name for group in drawing.sharing_groups.all()]
        json.append({
            'id': drawing.id,
            'uid': drawing.uid,
            'name': drawing.name,
            'description': drawing.description,
            'attributes': drawing.serialize_attributes,
            'sharing_groups': sharing_groups
        })
        
    shared_drawings = AOI.objects.shared_with_user(request.user)
    for drawing in shared_drawings:
        if drawing not in drawings:
            username = drawing.user.username
            actual_name = drawing.user.first_name + ' ' + drawing.user.last_name
            json.append({
                'id': drawing.id,
                'uid': drawing.uid,
                'name': drawing.name,
                'description': drawing.description,
                'attributes': drawing.serialize_attributes,
                'shared': True,
                'shared_by_username': username,
                'shared_by_name': actual_name
            })
        
    return HttpResponse(dumps(json))

'''
'''
def delete_drawing(request, uid):
    try:
        drawing_obj = get_feature_by_uid(uid)
    except Feature.DoesNotExist:
        raise Http404
    
    #check permissions
    viewable, response = drawing_obj.is_viewable(request.user)
    if not viewable:
        return response
        
    drawing_obj.delete()
    
    return HttpResponse("", status=200)

'''
'''
def get_clipped_shape(request):
    zero = .01

    if not (request.POST and request.POST['target_shape']):
        return HTTPResponse("No shape submitted", status=400)

    target_shape = request.POST['target_shape']    
    geom = GEOSGeometry(target_shape, srid=3857)

    clipped_shape = clip_to_grid(geom)

    # return new_shape['geometry__union']
    if clipped_shape and clipped_shape.area >= zero: #there was overlap
        largest_poly = LargestPolyFromMulti(clipped_shape)
        wkt = largest_poly.wkt
        return HttpResponse(dumps({"clipped_wkt": wkt}), status=200)
    else: 
        return HttpResponse("Submitted Shape is outside Grid Cell Boundaries (no overlap).", status=400)

    # return HttpResponse(dumps({"clipped_wkt": wkt}), status=200)    
    

'''
'''
def aoi_analysis(request, aoi_id):
    from aoi_analysis import display_aoi_analysis
    aoi_obj = get_object_or_404(AOI, pk=aoi_id)
    #check permissions
    viewable, response = aoi_obj.is_viewable(request.user)
    if not viewable:
        return response
    return display_aoi_analysis(request, aoi_obj)
    # Create your views here.

'''
'''    
def get_attributes(request, uid):
    try:
        scenario_obj = get_feature_by_uid(uid)
    except Scenario.DoesNotExist:
        raise Http404
    
    #check permissions
    viewable, response = scenario_obj.is_viewable(request.user)
    if not viewable:
        return response
    
    return HttpResponse(dumps(scenario_obj.serialize_attributes))    

'''
'''
def get_geometry_orig(request, uid):
    try:
        scenario_obj = get_feature_by_uid(uid)
        wkt = scenario_obj.geometry_orig.wkt
    except Scenario.DoesNotExist:
        raise Http404
    
    #check permissions
    viewable, response = scenario_obj.is_viewable(request.user)
    if not viewable:
        return response
    
    return HttpResponse(dumps({"geometry_orig": wkt}), status=200)


'''
'''
# def wind_analysis(request, wind_id):
#     from wind_analysis import display_wind_analysis
#     wind_obj = get_object_or_404(WindEnergySite, pk=wind_id)
#     #check permissions
#     viewable, response = wind_obj.is_viewable(request.user)
#     if not viewable:
#         return response
#     return display_wind_analysis(request, wind_obj)
#     # Create your views here.
