#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django import setup
from django.test.runner import DiscoverRunner

settings.configure(**{
    'DEBUG': True,
    'TEMPLATE_DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'text',
    ),
    'TEMPLATE_DIRS': (
        os.path.join(os.path.dirname(__file__), 'text', 'templates'),
        os.path.join(os.path.dirname(__file__), 'text', 'tests', 'templates'),
    ),
    'TEMPLATE_CONTEXT_PROCESSORS': (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.request',
    ),
    'MIDDLEWARE_CLASSES': (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        'text.middleware.TextMiddleware',
        'text.middleware.ToolbarMiddleware',
    ),
    'ROOT_URLCONF': 'text.tests.urls',
    'STATIC_URL': '/static/'
})


if __name__ == "__main__":
    setup()
    failures = DiscoverRunner(verbosity=1).run_tests(['text'])
    if failures:
        sys.exit(failures)
