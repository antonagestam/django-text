django-text
===========

|Join the chat at https://gitter.im/antonagestam/django-text|

Intuitive text editing for the Django Admin.

This project is in early development, will change rapidly and most
likely has bugs.

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

Add ``text.middleware.TextMiddleware`` to your middleware.

.. code:: python

    # settings.py

    MIDDLEWARE = (
        # ...
        'text.middleware.TextMiddleware',
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

    import text

    urlpatterns += url(r'^django_text/', include(text.urls))

Run ``migrate``.

.. code:: shell

    $ python manage.py migrate

Usage
-----

The ``editable`` tag
~~~~~~~~~~~~~~~~~~~~

Add ``editable`` tags to your templates.

.. code:: html

    <h1>{% editable "header" "My Header" %}</h1>

    <div class="content">
        {% editable "text_body" %}
    </div>

The ``editable`` tag takes a default text as the second argument. If no
default text is passed, the name of the text node (i.e. the first
argument) will be used if there is no corresponding text node in the
database.

The ``blockeditable`` tag
~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the ``blockeditable`` tag that let's you wrap content
to use as the default text.

.. code:: html

    <div class="content">
        <h1>
            {% blockeditable "header" %}
                Read My Awesome Text
            {% endblockeditable %}
        </h1>
        
        {% blockeditable "content" %}
            Put your default text here!
        {% endblockeditable %}
    </div>

The ``blockeditable`` tags works with translation tags inside of it. So
if you already have a translated site, you can wrap your content with
this tag and only add text nodes for some of the languages that you
support.

Specifying content type
~~~~~~~~~~~~~~~~~~~~~~~

Both the ``editable`` and the ``blockeditable`` tags support specifying
the content type of its default text.

.. code:: html

    {% editable "html_node" "<h1>Hello World!</h1>" "html" %}

    {% blockeditable "markdown_node" "markdown" %}
    # Hello there,

    I can have markdown in my templates!
    {% endblockeditable %}

If this is not provided both will default to raw text.

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
report bugs and propose features.

License
-------

Copyright (c) 2015 Anton Agestam. django-text is released under the MIT
license. See the LICENSE file for more information and licenses for
bundled code.

.. |Join the chat at https://gitter.im/antonagestam/django-text| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/antonagestam/django-text?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |The django-text toolbar| image:: /docs/printscreen_toolbar.png
.. |django-text in Django Admin| image:: /docs/printscreen_admin.png
