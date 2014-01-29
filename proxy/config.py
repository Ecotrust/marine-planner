# WSGI module for use with Apache mod_wsgi or gunicorn

# # uncomment the following lines for logging
# # create a log.ini with `mapproxy-util create -t log-ini`
# from logging.config import fileConfig
# import os.path
# fileConfig(r'/vagrant/log.ini', {'here': os.path.dirname(__file__)})
import os
from mapproxy.wsgiapp import make_wsgi_app

ROOT = os.path.dirname(os.path.realpath(__file__))

YAML = os.path.join(ROOT, 'mapproxy.yaml')
application = make_wsgi_app(YAML)
#application = make_wsgi_app('/vagrant/proxy/mapproxy.yaml')
