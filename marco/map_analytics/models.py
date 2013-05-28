from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from data_manager.models import Layer


class Entry(models.Model):
    user = models.ForeignKey(User, related_name='+')
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Entry, self).save(*args, **kwargs)

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