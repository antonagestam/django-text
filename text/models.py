from django.db import models
from django.conf import settings

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


class TextGetter(object):
    def __init__(self):
        self.registered_texts = set()
        self.texts = {}

    def register(self, text_name):
        self.registered_texts.add(text_name)

    def require(self, text_name, language):
        text_id = '%s_%s' % (text_name, language)
        if text_id not in self.texts:
            self.register(text_name)
            self.get_registered_texts()
        return self.texts[text_id]

    def get_registered_texts(self):
        texts = Text.objects.filter(name__in=self.registered_texts)
        for text in texts:
            self.texts[text.text_id] = text

    def clear(self, text):
        if text.text_id in self.texts:
            del self.texts[text.text_id]
        if text.name in self.registered_texts:
            self.registered_texts.remove(text.name)


text_getter = TextGetter()
