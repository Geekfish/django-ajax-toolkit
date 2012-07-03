from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import Resource

from django.contrib import messages


class MessageWrapper(object):
    def __init__(self, message):
        self.level = message.level
        self.message = unicode(message.message)
        self.extra_tags = message.tags

    def to_dict(self):
        return {
            'level': self.level,
            'message': self.message,
            'extra_tags': self.extra_tags,
        }

class MessageResource(Resource):
    level = fields.CharField(attribute='level')
    message = fields.CharField(attribute='message')
    extra_tags = fields.CharField(attribute='extra_tags')

    class Meta:
        resource_name = 'message'
        object_class = MessageWrapper
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = []

    def get_object_list(self, request=None, **kwargs):
        messages.info(request, 'Test info message')
        results = []
        for message in messages.get_messages(request):
            results.append(MessageWrapper(message))
        return results

    def detail_uri_kwargs(self, bundle_or_obj):
        return "foo/bar/1"

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list()

    def obj_get(self, request=None, **kwargs):
        pass

    def get_schema(self, request=None, **kwargs):
        return super(MessageResource, self).get_schema(request=request, **kwargs)
