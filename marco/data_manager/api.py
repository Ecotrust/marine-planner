from django.contrib.auth.models import User
from data_manager.models import Layer
from tastypie import fields
from tastypie.resources import ModelResource

class LayerResource(ModelResource):
    class Meta:
        queryset = Layer.objects.all()
        resource_name = 'layer'