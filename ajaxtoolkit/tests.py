# coding=UTF-8

from django.test import TestCase
from django.http import HttpRequest

from django.contrib import messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from hamcrest import *

from ajaxtoolkit.middleware import AjaxMiddleware
from ajaxtoolkit.http import JsonResponse

class JsonResponseTests(TestCase):

    def test_response_rendering(self):
        response = JsonResponse({'foo': 'bar'})
        response.render()
        assert_that(response.content, is_('{"foo": "bar"}'))

        response = JsonResponse({'foo': u'ελληνικά'})
        response.render()
        assert_that(response.content, is_('{"foo": "\u03b5\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac"}'))


class AjaxMiddlewareTests(TestCase):

    def test_middleware_appends_messages(self):
        request = HttpRequest()
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)

        message = "Hello. Yes. This is dog"
        messages.info(request, message)

        response = JsonResponse()
        middleware = AjaxMiddleware()
        processed_response = middleware.process_template_response(request, response)

        assert_that(processed_response.dict_content["django_messages"][0], has_entry("message", equal_to(message)))

