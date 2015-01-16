#!/usr/bin/python

import sys
import os
import json

remoteJSON = 'http://portal.midatlanticocean.org/media/data_manager/geojson/ArtificialReefsNoDecimals.json'
localFile = '/Users/sfletcher/dev/ofr-mp/cronjobs/test.json'

# Download JSON, extract the GeoJSON, save as local file, re-project to spherical mercator
def wget(url, filename):
    import urllib2
    try:
        req = urllib2.Request(url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        data = json.load(f)
    except Exception:
        import traceback
        logging.exception('generic exception: ' + traceback.format_exc())
    else:
        output = open(filename,'wb')
        output.write(json.dumps(data))
        output.close()
        # Re-Project from 4326 to 3857
        # ogr2ogr -f "GeoJSON" survey_results_2.json -t_srs "EPSG:3857" survey_results.json
        # Question can we re-project in place or do we need a temp file name (localFile and localTempFile)?

# Download the JSON
wget(remoteJSON, localFile)

