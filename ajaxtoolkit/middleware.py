from django.contrib import messages


class AjaxMiddleware(object):
    def process_template_response(self, request, response):
        should_append_messages = all((
            request.is_ajax(),
            getattr(response, 'message_support', False),
            hasattr(response, 'serializable_content')
            and isinstance(response.serializable_content, dict),
        ))
        if should_append_messages:
            django_messages = []

            for message in messages.get_messages(request):
                django_messages.append({ 
                    "level": message.level,
                    "message": unicode(message.message),
                    "extra_tags": message.tags,
                })
            response.serializable_content['django_messages'] = django_messages
        return response
