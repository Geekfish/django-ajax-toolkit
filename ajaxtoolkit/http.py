from django.http import HttpResponse
import msgpack

from ajaxtoolkit.jsonwrapper import json


class MessageInjectable(object):
    message_support = True


class AbstractSerializableResponse(HttpResponse, MessageInjectable):
    mimetype = None
    encoder = None
    default = None

    def __init__(self, serializable_content=None, mimetype=None, status=None, content_type=None):
        if mimetype is None:
            mimetype = self.mimetype
        self.serializable_content = serializable_content if serializable_content is not None else self.default
        super(AbstractSerializableResponse, self).__init__('', mimetype, status, content_type)

    def pre_encoding(self):
        pass

    def post_encoding(self):
        pass

    def render(self):
        self.pre_encoding()
        self.content = self.encoder.dumps(self.serializable_content)
        self.post_encoding()
        return self


class JsonResponse(AbstractSerializableResponse):
    mimetype = 'application/json'
    encoder = json


class MsgpackResponse(AbstractSerializableResponse):
    mimetype = 'application/x-msgpack'
    encoder = msgpack
