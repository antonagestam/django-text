#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-text',
    description='Intuitive text editing for the Django Admin.',
    version='1.4.0',
    long_description=open('README.md').read(),
    author='Anton Agestam',
    author_email='msn@antonagestam.se',
    packages=find_packages(),
    url='https://github.com/antonagestam/django-text/',
    license='The MIT License (MIT)',
    include_package_data=True,
    zip_safe=False,  # because we're including static files
    install_requires=['Django>=1.7.4', 'Markdown>=2.6', ],
    classifiers=['Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3']
)
