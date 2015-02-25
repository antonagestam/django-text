from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text

import markdown


MARKDOWN_TEMPLATE = u"""
<textarea{0}>\r\n{1}</textarea>
<div class="editor">{2}</div>
"""


class MarkdownEditorWidget(forms.widgets.Textarea):
    class Media:
        css = {
            'all': (
                'text/bundle/medium-editor-3.0.0/css/medium-editor.min.css',
                'text/bundle/medium-editor-3.0.0/css/themes/default.min.css',
                'text/css/markdown-widget.css',
                'http://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic&subset=latin,latin-ext',
            )
        }
        js = (
            'text/bundle/medium-editor-3.0.0/js/medium-editor.min.js',
            'text/bundle/he-0.5.0/he.js',
            'text/bundle/to-markdown-0.0.3/to-markdown.js',
            'text/bundle/medium-editor-markdown-1.1.0/me-markdown.no-deps.min.js',
            'text/js/markdown-widget.js',
        )

    def __init__(self, attrs=None):
        default_attrs = {'cols': '40', 'rows': '10', 'class': 'markdown', }
        if attrs:
            default_attrs.update(attrs)
        super(MarkdownEditorWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        rendered = mark_safe(markdown.markdown(value, output_format='html5'))
        return format_html(
            MARKDOWN_TEMPLATE,
            flatatt(final_attrs),
            force_text(value),
            rendered)
