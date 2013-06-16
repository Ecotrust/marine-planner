# Django settings for lot project.
from madrona.common.default_settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIME_ZONE = 'America/Vancouver'
ROOT_URLCONF = 'urls' 
LOGIN_REDIRECT_URL = '/visualize'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'marco',
        'USER': 'vagrant',
    }
}
 

LOG_FILE =  os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'mp.log'))


INSTALLED_APPS += ( 'general', 
                    'data_manager',
                    'mp_settings',
                    'explore',
                    'visualize',
                    'django.contrib.humanize',
                    'flatblocks',
                    'proxy'
                  )

GEOMETRY_DB_SRID = 99996
GEOMETRY_CLIENT_SRID = 3857 #for latlon
GEOJSON_SRID = 3857

#APP_NAME = "Marine Planner Data Portal"
#FEEDBACK_RECIPIENT = "Marine Planning Team <mp-team@marineplanner.org>"
#HELP_EMAIL = "mp-team@marineplanner.org"
#DEFAULT_FROM_EMAIL = "Marine Planning Team <mp-team@marineplanner.org>"

# url for socket.io printing
#SOCKET_URL = 'http://dev.marco.marineplanning.org:8080'

# Change the following line to True, to display the 'under maintenance' template
UNDER_MAINTENANCE_TEMPLATE = False

TEMPLATE_DIRS = ( os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')), )

import logging
logging.getLogger('django.db.backends').setLevel(logging.ERROR)

from settings_local import *
