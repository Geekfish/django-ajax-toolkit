#!/usr/bin/env python
import sys
from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            'django.contrib.messages',
            'ajaxtoolkit',
        ],
        TEMPLATE_CONTEXT_PROCESSORS=(
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.request",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.contrib.messages.context_processors.messages",
        ),
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.transaction.TransactionMiddleware',
        ),
        ROOT_URLCONF='',
        DEBUG=False,
    )

from django.test.simple import DjangoTestSuiteRunner


def runtests(*test_args):
    if not test_args:
        test_args = ['ajaxtoolkit']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    testrunner = DjangoTestSuiteRunner()
    failures = testrunner.run_tests(test_args, verbosity=1,
                                    interactive='--no-input' not in sys.argv)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
