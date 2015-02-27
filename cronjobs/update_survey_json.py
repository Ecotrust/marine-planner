#!/usr/bin/python
import sys
import os
import json

# remoteJSON = 'http://portal.midatlanticocean.org/media/data_manager/geojson/ArtificialReefsNoDecimals.json'
REMOTE_JSON = 'http://ofr-coastal-use.point97.io/reports/geojson/ofr-mapping-with-counts/q4'
# localFile = '/Users/sfletcher/dev/ofr-mp/cronjobs/test.json'
LOCAL_4326 = '../media/data_manager/geojson/survey_results_4326.json'
LOCAL_3857 = '../media/data_manager/geojson/survey_results_3857.json'
LOCAL_DATA = 'survey_results_unsummarized.json'

# Aquired the following categorizations from the OFRSurvey_Use_data_Categories document found here: https://drive.google.com/#folders/0By3VwnCJtq0rMkxpdjBEcEQ4Slk

### BOATER USE LAYER ###
BOATER_USE_LAYER = []
# Boating
BOATER_USE_LAYER.extend(['Motor', 'Sail', 'Kayak', 'Personal Watercraft', 'Research (boating)'])
# Recreational Fishing
BOATER_USE_LAYER.extend(['Private vessel (recreational fishing)', 'Charter vessel (recreational fishing)', 'Commercial/private vessel (commercial fishing)', 'Charter vessel (Fishing Charter Captain)', 'Charter vessel (Dive Boat Captain)'])
# Commercial Fishing
BOATER_USE_LAYER.extend(['Lobstering (commercial fishing)', 'Research (commercial fishing)', 'Research (recreational fishing)'])
# Diving by Boat
BOATER_USE_LAYER.extend(['Spearfishing (diving by boat)', 'Photography (diving by boat)', 'Pleasure (diving by boat)', 'Lobstering (diving by boat)', 'Collection for aquarium trade or for personal tank (diving by boat)', 'Research (diving by boat)'])
# Snorkel/freediving from vessel
BOATER_USE_LAYER.extend(['Spearfishing - commercial or recreational (snorkel/freediving from vessel)', 'Photography (snorkel/freediving from vessel)', 'Pleasure (snorkel/freediving from vessel)', 'Lobstering (snorkel/freediving from vessel)', 'Collection for aquarium trade or for personal tank (snorkel/freediving from vessel)', 'Research (snorkel/freediving from vessel)'])

### COMMERCIAL FISHING USE ###
COMMERCIAL_FISHING_USE = []
# Commercial Fishing
COMMERCIAL_FISHING_USE.extend(['Shore/pier (commercial fishing)', 'Commercial/private vessel (commercial fishing)', 'Charter vessel (Fishing Charter Captain)', 'Charter vessel (Dive Boat Captain)', 'Lobstering (commercial fishing)', 'Research (commercial fishing)'])

### EXTRACTIVE DIVING USE
EXTRACTIVE_DIVING_USE = []
# SCUBA diving from shore
EXTRACTIVE_DIVING_USE.extend(['Spearfishing (diving from shore)', 'Lobstering (diving from shore)', 'Collection for aquarium trade or for personal tank (diving from shore)'])
# SCUBA diving by boat
EXTRACTIVE_DIVING_USE.extend(['Lobstering (diving by boat)', 'Collection for aquarium trade or for personal tank (diving by boat)', 'Spearfishing (diving by boat)'])
# Snorkel/freediving from shore (includes kayak)
EXTRACTIVE_DIVING_USE.extend(['Spearfishing (snorkel/freediving from shore)', 'Lobstering (snorkel/freediving from shore', 'Collection for aquarium trade or for personal tank (snorkel/freediving from shore)'])
# Snorkel/freediving from vessel
EXTRACTIVE_DIVING_USE.extend(['Spearfishing - commercial or recreational (snorkel/freediving from vessel)', 'Lobstering (snorkel/freediving from vessel)', 'Collection for aquarium trade or for personal tank (snorkel/freediving from vessel)'])

### RECREATIONAL FISHING USE ###
RECREATIONAL_FISHING_USE = []
# Recreational Fishing
RECREATIONAL_FISHING_USE.extend(['Shore/pier (recreational fishing)', 'Private vessel (recreational fishing)', 'Charter vessel (recreational fishing)', 'Research (recreational fishing)'])
# Diving by Boat
RECREATIONAL_FISHING_USE.extend(['Spearfishing (diving by boat)', 'Lobstering (diving by boat)', 'Collection for aquarium trade or for personal tank (diving by boat)'])
# Snorkel/freediving from vessel
RECREATIONAL_FISHING_USE.extend(['Spearfishing - commercial or recreational (snorkel/freediving from vessel)', 'Lobstering (snorkel/freediving from vessel)', 'Collection for aquarium trade or for personal tank (snorkel/freediving from vessel)'])
# SCUBA diving from shore (includes kayak)
RECREATIONAL_FISHING_USE.extend(['Spearfishing (diving from shore)', 'Lobstering (diving from shore)', 'Collection for aquarium trade or for personal tank (diving from shore)'])
# Snorkel/freediving from shore (includes kayak)
RECREATIONAL_FISHING_USE.extend(['Spearfishing (snorkel/freediving from shore)', 'Lobstering (snorkel/freediving from shore', 'Collection for aquarium trade or for personal tank (snorkel/freediving from shore)'])

### RESEARCH USE ###
RESEARCH_USE = []
# Boating
RESEARCH_USE.extend(['Research (boating)'])
# Recreational fishing 
RESEARCH_USE.extend(['Research (recreational fishing)'])
# Commercial fishing
RESEARCH_USE.extend(['Research (commercial fishing)'])
# SCUBA diving from shore (includes kayak)
RESEARCH_USE.extend(['Research (diving from shore)'])
# SCUBA diving by boat
RESEARCH_USE.extend(['Research (diving by boat)'])
# Snorkel/freediving from shore (includes kayak)
RESEARCH_USE.extend(['Research (snorkel/freediving from shore)'])
# Snorkel/freediving from vessel
RESEARCH_USE.extend(['Research (snorkel/freediving from vessel)'])
# Other
RESEARCH_USE.extend(['Environmental Monitoring/inspection', 'Artificial reef construction'])

### SCUBA DIVING USE
SCUBA_DIVING_USE = []
# SCUBA diving from shore (includes kayak)
SCUBA_DIVING_USE.extend(['Spearfishing (diving from shore)', 'Photography (diving from shore)', 'Pleasure (diving from shore)', 'Lobstering (diving from shore)', 'Collection for aquarium trade or for personal tank (diving from shore)', 'Research (diving from shore)'])
# SCUBA diving by boat
SCUBA_DIVING_USE.extend(['Spearfishing (diving by boat)', 'Photography (diving by boat)', 'Pleasure (diving by boat)', 'Lobstering (diving by boat)', 'Collection for aquarium trade or for personal tank (diving by boat)', 'Research (diving by boat)'])

### SPEARFISHING USE
SPEARFISHING_USE = []
# SCUBA diving from shore
SPEARFISHING_USE.extend(['Spearfishing (diving from shore)'])
# SCUBA diving by boat
SPEARFISHING_USE.extend(['Spearfishing (diving by boat)'])
# Snorkel/freediving from shore (includes kayak)
SPEARFISHING_USE.extend(['Spearfishing (snorkel/freediving from shore)'])
# Snorkel/freediving from vessel
SPEARFISHING_USE.extend(['Spearfishing - commercial or recreational (snorkel/freediving from vessel)'])

### WATER SPORTS ###
WATER_SPORTS = ['Surfing', 'Kiteboarding', 'Stand-up paddle boarding', 'Windsurfing']

### USER CONFLICTS FOR DIVERS
# Will need to be manually generated by OFR folks

def getGeoJSON(data):
    return data['geoJson']

def transformGeometry(geojson, s_srs, t_srs):
    # Re-Project from 4326 to 3857
    # ogr2ogr -f "GeoJSON" survey_results_2.json -t_srs "EPSG:3857" survey_results.json
    import os
    command = "ogr2ogr -f \"GeoJSON\" " + LOCAL_3857 + " -t_srs \"EPSG:" + t_srs + "\" " + LOCAL_4326
    os.system(command)

def moveUniqueID(geojson): 
    features = geojson['features']
    for feature in features:
        feature['properties']['UniqueID'] = feature['UniqueID']

def summarizeActivities(geojson):
    features = geojson['features']
    for feature in features:
        properties = feature['properties']
        keys = properties.keys()
        for key in keys:
            if key != 'Total':
                # get activity category and count
                activity_count = properties[key]
                categories = getCategories(key)
                for category in categories:
                    # create category with count or add to category count
                    if category != 'Other':
                        if category not in properties.keys():
                            properties[category] = activity_count 
                        else:
                            properties[category] += activity_count               
            else:
                properties['Total Activity Days'] = properties[key]                
            # remove activity from properties
            del(properties[key])         
            # add UniqueID
            properties['UniqueID'] = feature['UniqueID']
        feature['properties'] = properties

def getCategories(activity):
    categories = [];
    activity = activity.strip()
    if ( activity in BOATER_USE_LAYER):
        categories.append('Boater Use')
    if activity in COMMERCIAL_FISHING_USE:
        categories.append('Commercial Fishing Use')
    if activity in EXTRACTIVE_DIVING_USE:
        categories.append('Extractive Diving Use')
    if activity in RECREATIONAL_FISHING_USE:
        categories.append('Recreational Fishing Use')
    if activity in RESEARCH_USE:
        categories.append('Research Use')
    if activity in SCUBA_DIVING_USE:
        categories.append('SCUBA Diving Use')
    if activity in SPEARFISHING_USE:
        categories.append('Spearfishing Use')
    if activity in WATER_SPORTS:
        categories.append('Water Sports')
    if len(categories) == 0:
        categories.append('Other')
    return categories

def addressDuplicates(geojson):
    features = geojson['features']
    ids = []
    new_features = []
    for f in features:
        if f['UniqueID'] not in ids:
            addressDuplicateProperties(f)
            ids.append(f['UniqueID'])
            new_features.append(f)
    geojson['features'] = new_features
    
def addressDuplicateProperties(feature):
    properties = feature['properties']
    new_properties = dict()
    for key,value in properties.items():
        k = key.strip()
        if k not in new_properties.keys():
            new_properties[k] = value
        else:
            new_properties[k] += value
    feature['properties'] = new_properties

# Download JSON, extract the GeoJSON, save as local file, re-project to spherical mercator
def wget():
    import urllib2
    try:
        req = urllib2.Request(REMOTE_JSON)
        opener = urllib2.build_opener()
        f = opener.open(req)
        data = json.load(f)
    except Exception:
        import traceback
        logging.exception('Exception thrown in update_survey_json: ' + traceback.format_exc())
    else:
        # grab geojson from endpoint data
        geojson = getGeoJSON(data)

        # create non-summarized data file
        try:
            os.remove(LOCAL_DATA)
        except OSError:
            pass
        # moveUniqueID(geojson)
        addressDuplicates(geojson) 
        output_data = open(LOCAL_DATA,'wb')
        output_data.write(json.dumps(geojson, indent=4))
        output_data.close()

        # summarize into categories
        summarizeActivities(geojson)

        # create local 4326 geojson
        try:
            os.remove(LOCAL_4326)
        except OSError:
            pass
        output_4326 = open(LOCAL_4326,'wb')
        output_4326.write(json.dumps(geojson, indent=4))
        output_4326.close()

        # create local 3857 geojson
        try:
            os.remove(LOCAL_3857)
        except OSError:
            pass
        transformGeometry(geojson, '4326', '3857')

# Download the JSON
wget()

