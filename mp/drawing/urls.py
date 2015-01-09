from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #drawings
    url(r'get_drawings$', get_drawings),
    url(r'delete_design/(?P<uid>[\w_]+)/$', delete_drawing), #user deletes drawing (or cancels empty geometry result)
    url(r'get_attributes/(?P<uid>[\w_]+)/$', get_attributes), #get attributes for a given scenario
    url(r'get_geometry_orig/(?P<uid>[\w_]+)/$', get_geometry_orig), #get geometry_orig wkt
    url(r'clip_to_grid$', get_clipped_shape),
    #feature reports
    # url(r'wind_report/(\d+)', wind_analysis, name='wind_analysis'), #user requested wind energy site analysis 
    url(r'aoi_report/(\d+)', aoi_analysis, name='aoi_analysis'), #user requested area of interest analysis 

)
