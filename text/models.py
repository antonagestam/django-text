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
        text_getter.clear(self)
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


class TextGetter(object):
    def __init__(self):
        self.registered_texts = {}
        self.texts = {}

    def register(self, text_name):
        language = get_language()
        subset_add(self.registered_texts, language, text_name)

    def require(self, text_name):
        language = get_language()
        if not in_sub(self.texts, language, text_name):
            self.register(text_name)
            self.get_registered_texts()
        return subdict_get(self.texts, language, text_name)

    def get_registered_texts(self):
        language = get_language()
        registered = self.registered_texts[language]
        if language not in self.texts:
            existing = set()
        else:
            existing = set(self.texts[language].keys())
        missing = registered - existing
        texts = Text.objects.filter(name__in=missing, language=language)
        for text in texts.iterator():
            subdict_add(self.texts, text.language, text.name, text)

    def clear(self, text):
        try:
            subdict_del(self.texts, text.language, text.name)
        except KeyError:
            pass

        try:
            subset_remove(self.registered_texts, text.language, text.name)
        except KeyError:
            pass


text_getter = TextGetter()


class TextSetter(object):
    def __init__(self):
        self.texts = {}

    def set(self, name, text):
        language = get_language()
        subdict_add(self.texts, language, name, text)

    def save(self):
        for language, texts in self.texts:
            for name, value in texts:
                text = Text(name=name, body=value, language=language)
                text.save()
        self.clear()

    def clear(self):
        self.texts = {}


text_setter = TextSetter()
