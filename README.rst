django-ajax-toolkit
===================

**Dependencies**

* msgpack-python>=0.2.4
* django>=1.3


**CI status (Travis)**

.. image:: https://api.travis-ci.org/Geekfish/django-ajax-toolkit.png?branch=master,release/0.1,release/0.2

Installation
------------

Grab it from pypi with::

    pip install django-ajax-toolkit

or::

    easy_install django-ajax-toolkit


Returning data objects in views
-------------------------------

JsonResponse
~~~~~~~~~~~~
If you want to extend your views to work with ajax you may choose to return json data in your response.
To make this easier you can use ``JsonResponse`` found in ``ajaxtoolkit.http``::

    from ajaxtoolkit.http import JsonResponse

    class MyView(TemplateView):

        def get(self, request, *args, **kwargs):
            if request.is_ajax:
                context = self.get_context_data()
                return JsonResponse(context)
            # ...

This will set the correct mimetype (``application/json``) and serialise your context data into a json object.


MsgpackResponse
~~~~~~~~~~~~~~~
``MsgpackResponse`` works in a similar way to ``JsonResponse``, but uses msgpack to provide with binary serialisation.
The usage is the same as with ``JsonResponse``::


    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            context = self.get_context_data()
            return MsgpackResponse(context)
        # ...


Ajax Middleware
---------------
If you're using Django's messages framework, you can also add ``ajaxtoolkit.middleware.AjaxMiddleware`` in your
middleware.
        

This will inject all messages generated in your request into your ``JsonResponse`` object::

    from django.contrib import messages
    from ajaxtoolkit.http import JsonResponse

    class MyView(TemplateView):

        def get(self, request, *args, **kwargs):
            if request.is_ajax:
                context = self.get_context_data()

                messages.info(request, "This is very useful")
                messages.warning(request, "Be careful!")

                return JsonResponse(context)
            # ...

This would be rendered as the following::

    {
        //...
        'django_messages': [
            {"extra_tags": "info",
             "message": "This is very useful",
             "level": 20},
            {"extra_tags": "warning",
             "message": "Be careful!",
             "level": 30}
        ]
    }


Bypassing the message middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to send an http response without attaching messages you can do that
by setting the ``message_support`` attribute of the response object::

    context = self.get_context_data()

    response = JsonResponse(context)
    response.message_support = False

    return response

You can also choose to subclass the original response classes, eg.::

    class MsgpackResponseWithoutMessages(MsgpackResponse):
        message_support = False

    # ...


Contribute
==========

Clone, create a virtualenv and run::

    make install

This will install all dependencies.  You can then run the tests with::

    ./runtests.py
