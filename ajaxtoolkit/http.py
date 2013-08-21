from django.http import HttpResponse
import msgpack

from ajaxtoolkit.jsonwrapper import json

class MessageInjectable(object):
    message_support = True


class AbstractDictionaryResponse(HttpResponse, MessageInjectable):
    MIMETYPE = None
    ENCODER = None

    def __init__(self, dict_content=None, mimetype=None, status=None, content_type=None):
        if mimetype is None:
            mimetype = self.MIMETYPE
        self.dict_content = dict_content if dict_content else {}
        if not isinstance(self.dict_content, dict):
            raise TypeError('The content argument must be or subclass dict type')
        super(AbstractDictionaryResponse, self).__init__('', mimetype, status, content_type)

    def pre_encoding(self):
        pass

    def post_encoding(self):
        pass

    def render(self):
        self.pre_encoding()
        self.content = self.ENCODER.dumps(self.dict_content)
        self.post_encoding()
        return self


class JsonResponse(AbstractDictionaryResponse):
    MIMETYPE = 'application/json'
    ENCODER = json


class MsgpackResponse(AbstractDictionaryResponse):
    MIMETYPE = 'application/x-msgpack'
    ENCODER = msgpack
