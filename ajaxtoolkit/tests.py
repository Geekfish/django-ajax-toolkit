# coding=UTF-8
import json
from hamcrest import *

from django.test import TestCase
from django.http import HttpRequest

from django.contrib import messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from ajaxtoolkit.middleware import AjaxMiddleware
from ajaxtoolkit.http import JsonResponse, MsgpackResponse


class SerializableResponseTest(TestCase):
    def test_default(self):
        class ResponseWithDefault(JsonResponse):
            default = {'result': 'default result'}

        class ResponseWithoutDefault(JsonResponse):
            pass

        response = ResponseWithDefault()
        response.render()
        assert_that(response.content, is_('{"result": "default result"}'))

        response = ResponseWithoutDefault()
        response.render()
        assert_that(response.content, is_("null"))


class JsonResponseTests(TestCase):

    def test_response_rendering(self):
        JsonResponse.encoder = json

        EXPECTED_CONTENT = '{"foo": "bar"}'
        EXPECTED_UNICODE_CONTENT = '{"foo": "\u03b5\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac"}'

        response = JsonResponse({'foo': 'bar'})
        response.render()
        assert_that(response.content, is_(EXPECTED_CONTENT))

        response = JsonResponse({'foo': u'ελληνικά'})
        response.render()
        assert_that(response.content, is_(EXPECTED_UNICODE_CONTENT))

    def test_content_type(self):
        response = JsonResponse({})
        self.assertEqual('application/json', response['Content-Type'])

    def test_list_content(self):
        response = JsonResponse([1,2,3])
        response.render()
        assert_that(response.content, is_("[1, 2, 3]"))


class MsgpackResponseTest(TestCase):
    def test_response_rendering(self):
        EXPECTED_CONTENT = b'\x81\xa3foo\xa3bar'
        EXPECTED_UNICODE_CONTENT = b'\x81\xa3foo\xb0\xce\xb5\xce\xbb\xce\xbb\xce\xb7\xce\xbd\xce\xb9\xce\xba\xce\xac'

        response = MsgpackResponse({'foo': 'bar'})
        response.render()
        assert_that(response.content, is_(EXPECTED_CONTENT))

        response = MsgpackResponse({'foo': u'ελληνικά'})
        response.render()
        assert_that(response.content, is_(EXPECTED_UNICODE_CONTENT))

    def test_content_type(self):
        response = MsgpackResponse({})
        self.assertEqual('application/x-msgpack', response['Content-Type'])


class AjaxMiddlewareTests(TestCase):
    def assert_django_messages_present(self, message, request, response):
        middleware = AjaxMiddleware()
        processed_response = middleware.process_template_response(request,
                                                                  response)
        assert_that(processed_response.serializable_content,
                    has_key("django_messages"))
        assert_that(processed_response.serializable_content["django_messages"][0],
                    has_entry("message", equal_to(message)))

    def test_middleware_appends_messages(self):
        request = HttpRequest()
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)

        message = "Hello. Yes. This is dog"
        messages.info(request, message)

        response = JsonResponse({})
        self.assert_django_messages_present(message, request, response)

        response = MsgpackResponse({})
        self.assert_django_messages_present(message, request, response)
