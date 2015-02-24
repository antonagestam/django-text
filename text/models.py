from django.db import models

import markdown


class Text(models.Model):
    TYPE_TEXT = 0
    TYPE_MARKDOWN = 1
    TYPES = (
        (TYPE_TEXT, 'Text'),
        (TYPE_MARKDOWN, 'Markdown'),
    )

    name = models.CharField(unique=True, max_length=50, db_index=True)
    body = models.TextField()
    type = models.IntegerField(choices=TYPES, blank=False, default=TYPE_TEXT)

    def __unicode__(self):
        return self.name

    def render(self):
        text = self.body
        if self.type is self.TYPE_MARKDOWN:
            text = markdown.markdown(text, output_format='html5')
        return text
