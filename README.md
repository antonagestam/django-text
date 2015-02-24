:warning:  This project is in early development and has bugs, contribution is welcome.

# django-text

Intuitive text editing for the Django Admin.

## Installation

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

## Usage

### Template tags

Add `editable` tags to your templates. Beware this tag will show the name
of the text node if there is no corresponding text nodes in the database.

```html
<h1>{% editable header %}</h1>

<div class="content">
    {% editable text_body %}
</div>
```

You can also use the `blockeditable` tag that let's you specify a default text
that will show up if there is no database entry.

```html
<div class="content">
    <h1>
        {% blockeditable header %}
            Read My Awesome Text
        {% endblockeditable %}
    </h1>
    
    {% blockeditable content %}
        Put your default text here!
    {% endblockeditable %}
</div>
```

The `blockeditable` tags works with translation tags inside of it. So if you already
have a translated site, you can wrap your content with this tag and only
add text nodes for some of the languages that you support.

### Content editing

Now add text nodes with the corresponding names in the Django Admin.
Currently raw text and [markdown](http://daringfireball.net/projects/markdown/) is supported.

![django-text in action](/docs/printscreen.png)
