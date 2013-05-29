from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to
from django.conf import settings
from tastypie.api import Api
from data_manager.api import LayerResource
from map_analytics.api import UserResource, LayerUseResource
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(LayerResource())
v1_api.register(UserResource())
v1_api.register(LayerUseResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    (r'^marco_profile/', include('marco_profile.urls')),
    #(r'^sdc/', include('scenarios.urls')),
    #(r'^drawing/', include('drawing.urls')),
    (r'^data_manager/', include('data_manager.urls')),
    #(r'^learn/', include('learn.urls')),
    #(r'^scenario/', include('scenarios.urls')),
    (r'^explore/', include('explore.urls')),
    (r'^visualize/', include('visualize.urls')),
    (r'^planner/', include('visualize.urls')),
    (r'^embed/', include('visualize.urls')),
    (r'^mobile/', include('visualize.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^$', redirect_to, {'url': '/portal/'}),
    (r'', include('madrona.common.urls')),    
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )