try:
    import ujson as json
except ImportError:
    from django.utils import simplejson as json
