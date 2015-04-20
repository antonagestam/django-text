django-text
===========

|Join the chat at https://gitter.im/antonagestam/django-text|
|Get downloads at https://pypi.python.org/pypi/django-text|
|See latest build status at https://circleci.com/gh/antonagestam/django-text/tree/master|
|Coverage|

Intuitive text editing for humans using Django.

This project is in early development, please test it out and report any bugs!


Installation
------------

Install the package with pip.

.. code:: shell

    $ pip install django-text

Add ``text`` to your installed packages.

.. code:: python

    # settings.py

    INSTALLED_APPS = (
        # ...
        'text',
    )

Add ``text.middleware.TextMiddleware`` and ``'text.middleware.ToolbarMiddleware'`` to your middleware classes.

.. code:: python

    # settings.py

    MIDDLEWARE_CLASSES = (
        # ...
        'text.middleware.TextMiddleware',
        'text.middleware.ToolbarMiddleware',
    )

Make sure these context processors are installed, they come with Django.

.. code:: python

    # settings.py

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.request',
    )

Append ``text.urls`` to your urlpatterns in ``urls.py``.

.. code:: python

    # urls.py

    from django.conf.urls import patterns, include, url

    from text.urls import urlpatterns as django_text_patterns
    
    
    urlpatterns = patterns('',
        url(r'^django_text/', include(django_text_patterns, namespace='django_text')),
    )

Run ``migrate``.

.. code:: shell

    $ python manage.py migrate


Usage
-----

The ``text`` tag
~~~~~~~~~~~~~~~~

Add ``editable`` tags to your templates.

.. code:: html

    {% load text %}

    <h1>{% text "header" "My Header" %}</h1>

    <div class="content">
        {% text "text_body" %}
    </div>

The ``text`` tag takes a default text as the second argument. If no
default text is passed, the name of the text node (i.e. the first
argument) will be used if there is no corresponding text node in the
database.

The ``blocktext`` tag
~~~~~~~~~~~~~~~~~~~~~

You can also use the ``blocktext`` tag that let's you wrap content
to use as the default text.

.. code:: html

    {% load text %}

    <div class="content">
        <h1>
            {% blocktext "header" %}
                Read My Awesome Text
            {% endblocktext %}
        </h1>
        
        {% blocktext "content" %}
            Put your default text here!
        {% endblocktext %}
    </div>

The ``blocktext`` tags works with translation tags inside of it. So
if you already have a translated site, you can wrap your content with
this tag and only add text nodes for some of the languages that you
support.

Specifying content type
~~~~~~~~~~~~~~~~~~~~~~~

Both the ``text`` and the ``blocktext`` tags support specifying
the content type of its default text. The choices are `"html"`,
`"markdown"` and `"text"` which is the default.

.. code:: html

    {% text "html_node" "<h1>Hello World!</h1>" "html" %}

    {% blocktext "markdown_node" "markdown" %}
    # Hello there,

    I can have markdown in my templates!
    {% endblocktext %}

If content type is not provided both will default to text.

Content editing
~~~~~~~~~~~~~~~

The toolbar allows you to edit texts directly on your pages. |The
django-text toolbar|

You can also edit texts in the Django Admin. |django-text in Django
Admin|

Missing text nodes will be added to the database automatically when
their template tags are rendered.


Settings
--------

**AUTOPOPULATE\_TEXT**

Default: ``True``

Set to false to disable django-text from adding missing text nodes to
the database.

**TEXT\_TOOLBAR\_ENABLED**

Default: ``True``

Set to false to disable the toolbar interface.

**TEXT\_TOOLBAR\_FORM\_PREFIX**

Default: ``'djtext_form'``

This is passed to the toolbar form and can be changed to avoid name
conflicts.

**TEXT\_TOOLBAR\_INSTANT\_UPDATE**

Default: ``True``

Set to false to disable instant updating of the DOM when saving texts in
the toolbar.

**TEXT\_INLINE\_WRAPPER**

Default: ``('<span data-text-name="{0}" class="{1}">', '</span>')``

A tuple of two that gets wrapped around texts in the template to enable
instant updating.

**TEXT\_INLINE\_WRAPPER\_CLASS**

Default: ``'dj_text_inline_wrapper'``

Change this to change the class of the element that gets wrapped around
texts.


Contribution
------------

Contribution is very welcome. Use
`issues <https://github.com/antonagestam/django-text/issues>`__ to
report bugs and propose features. For pull requests to be accepted
they need to be well tested.

Running tests
~~~~~~~~~~~~~

Install test dependencies.

.. code:: shell

    $ pip install -r test-requirements.txt

Run tests.

.. code:: shell

    $ export PYTHONPATH=`pwd`; runtests.py --settings='text.tests.settings'

Run tests with coverage.

.. code:: shell

    $ export PYTHONPATH=`pwd`; coverage run `which runtests.py` --settings='text.tests.settings'


License
-------

Copyright (c) 2015 Anton Agestam. django-text is released under the MIT
license. See the LICENSE file for more information and licenses for
bundled code.

.. |Join the chat at https://gitter.im/antonagestam/django-text| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/antonagestam/django-text?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Get downloads at https://pypi.python.org/pypi/django-text| image:: https://pypip.in/version/django-text/badge.svg
   :target: https://pypi.python.org/pypi/django-text
.. |See latest build status at https://circleci.com/gh/antonagestam/django-text/tree/master| image:: https://circleci.com/gh/antonagestam/django-text.png?style=shield
   :target: https://circleci.com/gh/antonagestam/django-text/tree/master
.. |The django-text toolbar| image:: /docs/printscreen_toolbar.png
.. |django-text in Django Admin| image:: /docs/printscreen_admin.png
.. |Coverage| image:: https://coveralls.io/repos/antonagestam/django-text/badge.svg?branch=master
   :target: https://coveralls.io/r/antonagestam/django-text?branch=master
