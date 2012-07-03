from django.conf.urls import include, url, patterns
from tastypie.api import Api
from ajaxtoolkit.plugins.tastypie.api import MessageResource


v1_api = Api(api_name='v1')
v1_api.register(MessageResource())

urlpatterns = patterns('',
    url('api/', include(v1_api.urls)),
)
