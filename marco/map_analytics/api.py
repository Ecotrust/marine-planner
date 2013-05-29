from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from data_manager.api import LayerResource
from data_manager.models import Layer
from models import LayerUse
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = []

class LayerUseResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True)
    layer = fields.ForeignKey(LayerResource, 'layer')

    class Meta:
        queryset = LayerUse.objects.all()
        resource_name = 'layeruse'        
        authentication = Authentication()
        authorization = Authorization()

    def obj_create(self, bundle, *args, **kwargs):
        try:
            bundle = super(LayerUseResource, self).obj_create(bundle, *args, **kwargs)
            if bundle.request.user and bundle.request.user.is_authenticated():
                bundle.obj.user = bundle.request.user
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('IntegrityError')
        return bundle        