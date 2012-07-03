from hamcrest import *
from tastypie.test import ResourceTestCase

from django.core.urlresolvers import reverse

class TestMessageResource(ResourceTestCase):
    urls = 'ajaxtoolkit.plugins.tastypie.test_urls'

    def testList(self):
        result = self.api_client.get(reverse('api_dispatch_list',
                kwargs={'resource_name': 'message', 'api_name': 'v1'})
)
        print result
