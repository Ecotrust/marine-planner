from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to
from django.conf import settings
from data_manager.api import LayerResource, ThemeResource
from tastypie.api import Api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import visualize
import explore
#from mapproxy.views import proxy_view
#import map_proxy
# print dir(map_proxy)
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(LayerResource())
v1_api.register(ThemeResource())


urlpatterns = patterns('',
                       (r'^api/', include(v1_api.urls)),
                       (r'^mp_profile/', include('mp_profile.urls')),
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
                       (r'^proxy/', include('mp_proxy.urls')),
                       url(r'^mapproxy/(?P<path>.*)',
                           'map_proxy.views.mapproxy_view'),
                       (r'^([\w-]*)/planner/', visualize.views.show_planner),
                       (r'^([\w-]*)/visualize/', visualize.views.show_planner),
                       (r'^([\w-]*)/embed/',
                        visualize.views.show_embedded_map),
                       (r'^([\w-]*)/catalog/', explore.views.data_catalog),
                       (r'^$', redirect_to, {'url': '/visualize/'}),
                       (r'', include('madrona.common.urls')),
                       )


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
