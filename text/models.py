from django.db import models
from django.conf import settings
from django.utils.translation import get_language

import markdown


class Text(models.Model):
    TYPE_TEXT = 0
    TYPE_MARKDOWN = 1
    TYPES = (
        (TYPE_TEXT, 'Text'),
        (TYPE_MARKDOWN, 'Markdown'),
    )

    name = models.CharField(max_length=50, db_index=True)
    body = models.TextField()
    type = models.IntegerField(
        choices=TYPES, blank=False, default=TYPE_MARKDOWN)
    language = models.CharField(
        choices=settings.LANGUAGES,
        max_length=5,
        default=settings.LANGUAGE_CODE)

    class Meta:
        unique_together = ('name', 'language', )
        index_together = ['name', 'language', ]
        ordering = ('name', 'language', )

    def __unicode__(self):
        return self.text_id

    def render(self):
        text = self.body
        if self.type is self.TYPE_MARKDOWN:
            text = markdown.markdown(text, output_format='html5')
        return text

    def save(self, *args, **kwargs):
        ret_val = super(Text, self).save(*args, **kwargs)
        return ret_val

    @property
    def text_id(self):
        return "%s_%s" % (self.name, self.language)


def subdict_add(obj, sub, key, value):
    if sub not in obj:
        obj[sub] = {}
    obj[sub][key] = value


def subdict_get(obj, sub, key):
    return obj[sub][key]


def subdict_del(obj, sub, key):
    del obj[sub][key]


def in_sub(obj, sub, key):
    return sub in obj and key in obj[sub]


def subset_add(obj, sub, value):
    if sub not in obj:
        obj[sub] = set()
    obj[sub].add(value)


def subset_remove(obj, sub, value):
    obj[sub].remove(value)


class TextSetter(object):
    def __init__(self):
        self.texts = {}

    def set(self, name, text):
        language = get_language()
        subdict_add(self.texts, language, name, text)

    def save(self):
        for language, texts in self.texts.iteritems():
            for name, value in texts.iteritems():
                text = Text(
                    name=name,
                    body=value,
                    language=language,
                    type=Text.TYPE_TEXT)
                text.save()
        self.clear()

    def clear(self):
        self.texts = {}


text_setter = TextSetter()
