# django-text

Edit content in the Django Admin.

## Installation and usage

Install the package with pip.

```shell
$ pip install django-text
```

Add `'text'` to your installed packages.

```python
# settings.py

INSTALLED_APPS = (
    # ...
    'text',
)
```

Run `migrate`.

```shell
$ python manage.py migrate
```

Add `editable` tags to your templates.

```html
<h1>{% editable header %}</h1>

<div class="content">
    {% editable text_body %}
</div>
```

Now add text nodes with the corresponding names in the Django Admin.
Currently raw text and [markdown](http://daringfireball.net/projects/markdown/) is supported.
