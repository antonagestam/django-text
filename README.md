# django-text

[![Join the chat at https://gitter.im/antonagestam/django-text](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/antonagestam/django-text?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Intuitive text editing for the Django Admin.

:warning:

This project is in early development, will change rapidly and most likely has bugs.


## Installation

Install the package with pip.

```shell
$ pip install django-text
```

Add `text` to your installed packages.

```python
# settings.py

INSTALLED_APPS = (
    # ...
    'text',
)
```

Add `text.middleware.TextMiddleware` to your middleware.

```python
# settings.py

MIDDLEWARE = (
    # ...
    'text.middleware.TextMiddleware',
)
```

Make sure these context processors are installed, they come with Django.

```python
# settings.py

TEMPLATE_CONTEXT_PROCESSORS = (
    # ...
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)
```

Append `text.urls` to your urlpatterns in `urls.py`.

```python
# urls.py

import text

urlpatterns += url(r'^django_text/', include(text.urls))
```


Run `migrate`.

```shell
$ python manage.py migrate
```


## Usage

### The `editable` tag

Add `editable` tags to your templates.

```html
<h1>{% editable "header" "My Header" %}</h1>

<div class="content">
    {% editable "text_body" %}
</div>
```

The `editable` tag takes a default text as the second argument.
If no default text is passed, the name of the text node (i.e. the first argument)
will be used if there is no corresponding text node in the database.


### The `blockeditable` tag

You can also use the `blockeditable` tag that let's you wrap content to use
as the default text.

```html
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
```

The `blockeditable` tags works with translation tags inside of it. So if you already
have a translated site, you can wrap your content with this tag and only
add text nodes for some of the languages that you support.


### Specifying content type

Both the `editable` and the `blockeditable` tags support specifying the content
type of its default text.

```html
{% editable "html_node" "<h1>Hello World!</h1>" "html" %}

{% blockeditable "markdown_node" "markdown" %}
# Hello there,

I can have markdown in my templates!
{% endblockeditable %}
```

If this is not provided both will default to raw text.


### Content editing

The toolbar allows you to edit texts directly on your pages.
![The django-text toolbar](/docs/printscreen_toolbar.png)

You can also edit texts in the Django Admin.
![django-text in Django Admin](/docs/printscreen_admin.png)

Missing text nodes will be added to the database automatically when their
template tags are rendered.


## Settings

__AUTOPOPULATE_TEXT__

Default: `True`

Set to false to disable django-text from adding missing text nodes to the database.

__TEXT_TOOLBAR_ENABLED__

Default: `True`

Set to false to disable the toolbar interface.

__TEXT_TOOLBAR_FORM_PREFIX__

Default: `'djtext_form'`

This is passed to the toolbar form and can be changed to avoid name conflicts.

__TEXT_TOOLBAR_INSTANT_UPDATE__

Default: `True`

Set to false to disable instant updating of the DOM when saving texts in the toolbar.

__TEXT_INLINE_WRAPPER__

Default: `('<span data-text-name="{0}" class="{1}">', '</span>')`

A tuple of two that gets wrapped around texts in the template to enable instant updating.

__TEXT_INLINE_WRAPPER_CLASS__

Default: `'dj_text_inline_wrapper'`

Change this to change the class of the element that gets wrapped around texts.


## Contribution

Contribution is very welcome. Use [issues](https://github.com/antonagestam/django-text/issues) to report bugs and propose features.


## License

Copyright (c) 2015 Anton Agestam. django-text is released under the MIT license.
See the LICENSE file for more information and licenses for bundled code.
