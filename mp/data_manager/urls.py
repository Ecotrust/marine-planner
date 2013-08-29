from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^layer/([A-Za-z0-9_-]+)$', update_layer),
    (r'^layer', create_layer),
    (r'^wa_config', load_config),
    (r'^get_json/([\w-]*)', get_json)
)
