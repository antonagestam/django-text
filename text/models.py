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
    type = models.IntegerField(choices=TYPES, blank=False, default=TYPE_TEXT)
    language = models.CharField(
        choices=settings.LANGUAGES,
        max_length=5,
        default=settings.LANGUAGE_CODE)

    class Meta:
        unique_together = ('name', 'language', )
        index_together = ['name', 'language', ]

    def __unicode__(self):
        return self.name

    def render(self):
        text = self.body
        if self.type is self.TYPE_MARKDOWN:
            text = markdown.markdown(text, output_format='html5')
        return text

    def save(self, *args, **kwargs):
        ret_val = super(Text, self).save(*args, **kwargs)
        text_getter.clear(self.name)
        return ret_val


class TextGetter(object):
    def __init__(self):
        self.registered_texts = set()
        self.texts = {}

    def register(self, text_name):
        self.registered_texts.add(text_name)

    def require(self, text_name):
        if text_name not in self.texts:
            self.register(text_name)
            self.get_registered_texts()
        return self.texts[text_name]

    def get_registered_texts(self):
        texts = Text.objects.filter(name__in=self.registered_texts)
        for text in texts:
            self.texts[text.name] = text

    def clear(self, text_name):
        del self.texts[text_name]


text_getter = TextGetter()
