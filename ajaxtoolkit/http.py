from django.http import HttpResponse
import simplejson as json
import msgpack


class MessageInjectable(object):
    message_support = True


class AbstractDictionaryResponse(HttpResponse, MessageInjectable):
    MIMETYPE = None
    ENCODER = None

    def __init__(self, dict_content=None, mimetype=MIMETYPE, status=None, content_type=None):
        self.dict_content = dict_content if dict_content else {}
        if type(self.dict_content) is not dict:
            raise TypeError('The content argument must be a dictionary')
        super(AbstractDictionaryResponse, self).__init__('', mimetype, status, content_type)


    def render(self):
        self.content = self.ENCODER.dumps(self.dict_content)
        return self


class JsonResponse(AbstractDictionaryResponse):
    MIMETYPE = 'application/json'
    ENCODER = json


class MsgpackResponse(AbstractDictionaryResponse):
    MIMETYPE = 'application/x-msgpack'
    ENCODER = msgpack
