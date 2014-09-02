# Create your views here.
from django.contrib.auth.models import Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import os
from querystring_parser import parser
import simplejson

from simplejson import dumps
from social.backends.google import GooglePlusAuth
from madrona.features import get_feature_by_uid

import settings

from models import *
from data_manager.models import *
from mp_settings.models import *

def show_planner(request, project=None, template='planner.html'):
    try:
        socket_url = settings.SOCKET_URL
    except AttributeError:
        socket_url = ''
    try:
        if project:
            mp_settings = MarinePlannerSettings.objects.get(slug_name=project)
        else:
            mp_settings = MarinePlannerSettings.objects.get(active=True)
        project_name = mp_settings.project_name
        latitude = mp_settings.latitude
        longitude = mp_settings.longitude
        zoom = mp_settings.zoom
        default_hash = mp_settings.default_hash
        min_zoom = mp_settings.min_zoom
        max_zoom = mp_settings.max_zoom
        project_logo = mp_settings.project_logo
        try:
            if project_logo:
                url_validator = URLValidator()
                url_validator(project_logo)
        except ValidationError, e:
            project_logo = os.path.join(settings.MEDIA_URL, project_logo)
        project_icon = mp_settings.project_icon
        try:
            url_validator = URLValidator()
            url_validator(project_icon)
        except ValidationError, e:
            project_icon = os.path.join(settings.MEDIA_URL, project_icon)
        project_home_page = mp_settings.project_home_page
        enable_drawing = mp_settings.enable_drawing
        bitly_registered_domain = mp_settings.bitly_registered_domain
        bitly_username = mp_settings.bitly_username
        bitly_api_key = mp_settings.bitly_api_key
    except:
        project_name = project_logo = project_icon = project_home_page = bitly_registered_domain = bitly_username = bitly_api_key = default_hash = ""
        latitude = longitude = zoom = min_zoom = max_zoom = None
        enable_drawing = False
    context = {
        'MEDIA_URL': settings.MEDIA_URL, 'SOCKET_URL': socket_url, 'login': 'true',
        'project_name': project_name, 'latitude': latitude, 'longitude': longitude, 'zoom': zoom,
        'default_hash': default_hash, 'min_zoom': min_zoom, 'max_zoom': max_zoom,
        'project_logo': project_logo, 'project_icon': project_icon, 'project_home_page': project_home_page,
        'enable_drawing': enable_drawing,
        'bitly_registered_domain': bitly_registered_domain, 'bitly_username': bitly_username, 'bitly_api_key': bitly_api_key
    }
    if request.user.is_authenticated:
        context['session'] = request.session._session_key
    if request.user.is_authenticated() and request.user.social_auth.all().count() > 0:
        context['picture'] = request.user.social_auth.all()[0].extra_data.get('picture')
    if settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY:
        context['plus_scope'] = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
        context['plus_id'] = settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY
    if settings.UNDER_MAINTENANCE_TEMPLATE:
        return render_to_response('under_maintenance.html',
                                  RequestContext(request, context))
    return render_to_response(template, RequestContext(request, context))

def show_embedded_map(request, project=None, template='map.html'):
    try:
        if project:
            mp_settings = MarinePlannerSettings.objects.get(slug_name=project)
        else:
            mp_settings = MarinePlannerSettings.objects.get(active=True)
        project_name = mp_settings.project_name
        project_logo = mp_settings.project_logo
        try:
            if project_logo:
                url_validator = URLValidator(verify_exists=False)
                url_validator(project_logo)
        except ValidationError, e:
            project_logo = os.path.join(settings.MEDIA_URL, project_logo)        
        project_home_page = mp_settings.project_home_page
    except:
        project_name = project_logo = project_home_page = None
    context = {
        'MEDIA_URL': settings.MEDIA_URL, 
        'project_name': project_name,
        'project_logo': project_logo, 
        'project_home_page': project_home_page 
    }
    #context = {'MEDIA_URL': settings.MEDIA_URL}
    return render_to_response(template, RequestContext(request, context)) 
    
def show_mobile_map(request, project=None, template='mobile-map.html'):
    try:
        if project:
            mp_settings = MarinePlannerSettings.objects.get(slug_name=project)
        else:
            mp_settings = MarinePlannerSettings.objects.get(active=True)
        print 'so far so good'
        project_name = mp_settings.project_name
        project_logo = mp_settings.project_logo
        print project_name
        print project_logo
        # try:
        #     if project_logo:
        #         url_validator = URLValidator(verify_exists=False)
        #         url_validator(project_logo)
        # except ValidationError, e:
        #     project_logo = os.path.join(settings.MEDIA_URL, project_logo) 
        print 'almost there...'       
        project_home_page = mp_settings.project_home_page
        print 'here we go...'
        latitude = mp_settings.latitude
        print latitude
        longitude = mp_settings.longitude
        print longitude
        zoom = mp_settings.zoom
        print zoom
        min_zoom = mp_settings.min_zoom
        max_zoom = mp_settings.max_zoom
        print min_zoom
        print max_zoom
    except:
        project_name = project_logo = project_home_page = None
    context = {
        'MEDIA_URL': settings.MEDIA_URL, 
        # 'project_name': project_name,
        # 'project_logo': project_logo, 
        # 'project_home_page': project_home_page 
        'latitude': latitude,
        'longitude': longitude,
        'zoom': zoom
    }
    #context = {'MEDIA_URL': settings.MEDIA_URL}
    return render_to_response(template, RequestContext(request, context)) 
    
def get_sharing_groups(request):
    from madrona.features import user_sharing_groups
    from functools import cmp_to_key
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    json = []
    sharing_groups = user_sharing_groups(request.user)
    for group in sharing_groups:
        members = []
        for user in group.user_set.all():
            if user.first_name.replace(' ', '') != '' and user.last_name.replace(' ', '') != '':
                members.append(user.first_name + ' ' + user.last_name)
            else:
                members.append(user.username)
        sorted_members = sorted(members, key=cmp_to_key(locale.strcoll))
        json.append({
            'group_name': group.name,
            'group_slug': slugify(group.name)+'-sharing',
            'members': sorted_members
        })
    return HttpResponse(dumps(json))    
     
'''
'''    
def share_bookmark(request):
    group_names = request.POST.getlist('groups[]')
    bookmark_uid = request.POST['bookmark']
    bookmark = get_feature_by_uid(bookmark_uid)
    
    viewable, response = bookmark.is_viewable(request.user)
    if not viewable:
        return response
        
    #remove previously shared with groups, before sharing with new list
    bookmark.share_with(None)
    
    groups = []
    for group_name in group_names:
        groups.append(Group.objects.get(name=group_name))
        
    bookmark.share_with(groups, append=False)
    
    return HttpResponse("", status=200)
    
'''
'''    
def get_bookmarks(request):
    #sync the client-side bookmarks with the server side bookmarks
    #update the server-side bookmarks and return the new list
    try:        
        bookmark_dict = parser.parse(request.POST.urlencode())['bookmarks']
    except:
        bookmark_dict = {}
    try:
        #loop through the list from the client
        #if user, bm_name, and bm_state match then skip 
        #otherwise, add to the db
        for key,bookmark in bookmark_dict.items():
            try:
                Bookmark.objects.get(user=request.user, name=bookmark['name'], url_hash=bookmark['hash'])
            except Bookmark.DoesNotExist:
                new_bookmark = Bookmark(user=request.user, name=bookmark['name'], url_hash=bookmark['hash'])
                new_bookmark.save()
            except: 
                continue
    
        #grab all bookmarks belonging to this user 
        #serialize bookmarks into 'name', 'hash' objects and return simplejson dump 
        content = []
        bookmark_list = Bookmark.objects.filter(user=request.user)
        for bookmark in bookmark_list:
            sharing_groups = [group.name for group in bookmark.sharing_groups.all()]
            content.append({ 
                'uid': bookmark.uid, 
                'name': bookmark.name,
                'hash': bookmark.url_hash, 
                'sharing_groups': sharing_groups
            })
        
        shared_bookmarks = Bookmark.objects.shared_with_user(request.user)
        for bookmark in shared_bookmarks:
            if bookmark not in bookmark_list:
                username = bookmark.user.username
                actual_name = bookmark.user.first_name + ' ' + bookmark.user.last_name
                content.append({
                    'uid': bookmark.uid,
                    'name': bookmark.name,
                    'hash': bookmark.url_hash, 
                    'shared': True,
                    'shared_by_username': username,
                    'shared_by_name': actual_name
                })
        return HttpResponse(simplejson.dumps(content), mimetype="application/json", status=200)
    except:
        return HttpResponse(status=304)
    
def remove_bookmark(request): 
    try:
        bookmark_uid = request.POST['uid']
        bookmark = get_feature_by_uid(bookmark_uid)
        
        viewable, response = bookmark.is_viewable(request.user)
        if not viewable:
            return response
        
        bookmark.delete()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=304)

def add_bookmark(request):
    try:
        bookmark = Bookmark(user=request.user, name=request.POST.get('name'), url_hash=request.POST.get('hash'))
        bookmark.save()
        sharing_groups = [group.name for group in bookmark.sharing_groups.all()]
        content = []
        content.append({
            'uid': bookmark.uid,
            'name': bookmark.name, 
            'hash': bookmark.url_hash, 
            'sharing_groups': sharing_groups
        })
        print 'returning content'
        return HttpResponse(simplejson.dumps(content), mimetype="application/json", status=200)
    except:
        return HttpResponse(status=304)
        