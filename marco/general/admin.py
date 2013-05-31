from django.contrib import admin
from models import MarinePlannerSettings 

class MarinePlannerSettingsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'latitude', 'longitude', 'zoom', 'active')
    search_fields = ['project_name']
    ordering = ('project_name',)

admin.site.register(MarinePlannerSettings, MarinePlannerSettingsAdmin)

from madrona.news.models import Entry, Tag
admin.site.unregister(Entry)
admin.site.unregister(Tag)

from madrona.screencasts.models import Screencast, YoutubeScreencast
admin.site.unregister(Screencast)
admin.site.unregister(YoutubeScreencast)

from madrona.studyregion.models import StudyRegion
admin.site.unregister(StudyRegion)

from madrona.simplefaq.models import FaqGroup, Faq
admin.site.unregister(FaqGroup)
admin.site.unregister(Faq)

from madrona.layers.models import PrivateKml, PublicLayerList
admin.site.unregister(PrivateKml)
admin.site.unregister(PublicLayerList)

from madrona.staticmap.models import MapConfig
admin.site.unregister(MapConfig)

from madrona.user_profile.models import UserProfile
admin.site.unregister(UserProfile)

from registration.models import RegistrationProfile
admin.site.unregister(RegistrationProfile)

from djcelery.models import TaskState, WorkerState, IntervalSchedule, CrontabSchedule, PeriodicTask
admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
