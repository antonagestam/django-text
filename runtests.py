#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django import setup

settings.configure(**{
    'DEBUG': True,
    'TEMPLATE_DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    'INSTALLED_APPS': ('text', ),
    'TEMPLATE_DIRS': (
        os.path.join(os.path.dirname(__file__), 'text', 'templates'),
    ),
    'TEMPLATE_CONTEXT_PROCESSORS': (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.request',
    ),
    'MIDDLEWARE_CLASSES': (
        'text.middleware.TextMiddleware',
        'text.middleware.ToolbarMiddleware',
    ),
    'ROOT_URLCONF': 'text.urls',
})

try:
    # Django <= 1.8
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner(verbosity=1)
except ImportError:
    # Django >= 1.8
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1)

if __name__ == "__main__":
    setup()
    failures = test_runner.run_tests(['text'])
    if failures:
        sys.exit(failures)
