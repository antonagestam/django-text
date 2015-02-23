#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-text',
    description='django-text',
    version='1.0.0',
    long_description=open('README.md').read(),
    author='Anton Agestam',
    author_email='msn@antonagestam.se',
    packages=find_packages(),
    url='https://github.com/antonagestam/django-text/',
    license='The MIT License (MIT)',
    include_package_data=True,
    install_requires=['Django>=1.7.4', 'Markdown>=2.6', ],
    classifiers=['Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3']
)
