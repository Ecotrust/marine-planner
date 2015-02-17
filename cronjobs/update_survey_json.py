#!/usr/bin/python

import sys
import os
import json

# remoteJSON = 'http://portal.midatlanticocean.org/media/data_manager/geojson/ArtificialReefsNoDecimals.json'
remoteJSON = 'http://ofr-coastal-use.point97.io/reports/geojson/ofr-mapping-with-counts/q4'
# localFile = '/Users/sfletcher/dev/ofr-mp/cronjobs/test.json'
local4326 = '../media/data_manager/geojson/survey_results_4326.json'
local3857 = '../media/data_manager/geojson/survey_results_3857.json'

# Download JSON, extract the GeoJSON, save as local file, re-project to spherical mercator
def wget():
    import urllib2
    try:
        req = urllib2.Request(remoteJSON)
        opener = urllib2.build_opener()
        f = opener.open(req)
        data = json.load(f)
    except Exception:
        import traceback
        logging.exception('Exception thrown in update_survey_json: ' + traceback.format_exc())
    else:
        geojson = getGeoJSON(data)
        summarizeActivities(geojson)
        # remove existing files (GeoJSON driver does not overwrite existing files)
        os.remove(local4326);
        os.remove(local3857);
        output = open(local4326,'wb')
        output.write(json.dumps(geojson, indent=4))
        output.close()
        transformGeometry(geojson, '4326', '3857')

def getGeoJSON(data):
    return data['geoJson']

def transformGeometry(geojson, s_srs, t_srs):
    # Re-Project from 4326 to 3857
    # ogr2ogr -f "GeoJSON" survey_results_2.json -t_srs "EPSG:3857" survey_results.json
    import os
    command = "ogr2ogr -f \"GeoJSON\" " + local3857 + " -t_srs \"EPSG:" + t_srs + "\" " + local4326
    os.system(command)

def summarizeActivities(geojson):
    features = geojson['features']
    for feature in features:
        properties = feature['properties']
        keys = properties.keys()
        for key in keys:
            if key != 'Total':
                # get activity category and count
                activity_count = properties[key]
                category = getCategory(key)
                # create category with count or add to category count
                if category in properties.keys():
                    properties[category] += activity_count
                else:
                    properties[category] = activity_count
                # remove activity from properties
            else:
                properties['Total Activity Days'] = properties[key]
            del(properties[key])
        feature['properties'] = properties

def getCategory(activity):
    if activity in ['Motor', 'Sail', 'Kayak', 'Personal Watercraft', 'Research (boating)']:
        return 'Boating'
    elif activity in ['Shore/pier (recreational fishing)', 'Private vessel (recreational fishing)', 'Charter vessel (recreational fishing)', 'Research (recreational fishing)']:
        return 'Recreational fishing'
    elif activity in ['Shore/pier (commercial fishing)', 'Commercial/private vessel (commercial fishing)', 'Charter vessel (Fishing Charter Captain)', 'Charter vessel (Dive Boat Captain)', 'Lobstering (commercial fishing)', 'Research (commercial fishing)']:
        return 'Commercial fishing'
    elif activity in ['Spearfishing (diving from shore)', 'Photography (diving from shore)', 'Pleasure (diving from shore)', 'Lobstering (diving from shore)', 'Collection for aquarium trade or for personal tank (diving from shore)', 'Research (diving from shore)']:
        return 'SCUBA diving from shore (includes kayak)'
    elif activity in ['Spearfishing (diving by boat)', 'Photography (diving by boat)', 'Pleasure (diving by boat)', 'Lobstering (diving by boat)', 'Collection for aquarium trade or for personal tank (diving by boat)', 'Research (diving by boat)']:
        return 'SCUBA diving by boat'
    elif activity in ['Spearfishing (snorkel/freediving from shore)', 'Photography (snorkel/freediving from shore)', 'Pleasure (snorkel/freediving from shore)', 'Lobstering (snorkel/freediving from shore)', 'Collection for aquarium trade or for personal tank (snorkel/freediving from shore)', 'Research (snorkel/freediving from shore)']:
        return 'Snorkel/freediving from shore (includes kayak)'
    elif activity in ['Spearfishing - commercial or recreational (snorkel/freediving from vessel)', 'Photography (snorkel/freediving from vessel)', 'Pleasure (snorkel/freediving from vessel)', 'Lobstering (snorkel/freediving from vessel)', 'Collection for aquarium trade or for personal tank (snorkel/freediving from vessel)', 'Research (snorkel/freediving from vessel)']:
        return 'Snorkel/freediving from vessel'
    elif activity in ['Surfing', 'Kiteboarding', 'Stand-up paddle boarding', 'Windsurfing']:
        return 'Watersports'
    else:
        return 'Other'

# Download the JSON
wget()

