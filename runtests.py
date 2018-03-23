#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django import setup
from django.test.runner import DiscoverRunner

settings.configure(**{
    'DEBUG': True,
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
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': (
                os.path.join(os.path.dirname(__file__), 'text', 'templates'),
                os.path.join(os.path.dirname(__file__), 'text', 'tests', 'templates'),
            ),
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.request',
                ],
                'debug': True,
            },
        },
    ],
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
