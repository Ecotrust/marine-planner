from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from data_manager.models import Layer

class LayerUse(models.Model):
    user = models.ForeignKey(User, related_name='+', null=True)
    date = models.DateTimeField(default=now)
    layer = models.ForeignKey(Layer, related_name='+')

    def __unicode__(self):
        if not self.user:
            username = "anonymous"
        else:
            username = self.user.username
        return username+' - '+self.layer.name