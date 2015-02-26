from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

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
        return mark_safe(text)

    def save(self, *args, **kwargs):
        ret_val = super(Text, self).save(*args, **kwargs)
        return ret_val

    @property
    def text_id(self):
        return "%s_%s" % (self.name, self.language)
