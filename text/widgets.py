from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text

from text.models import Text


MARKDOWN_TEMPLATE = u"""
<textarea{0}>\r\n{1}</textarea>
<div class="djtext_html_editor">{2}</div>
"""


class HTMLEditorWidget(forms.widgets.Textarea):
    class Media:
        css = {
            'all': (
                'text/bundle/medium-editor-3.0.0/css/medium-editor.min.css',
                'text/bundle/medium-editor-3.0.0/css/themes/default.min.css',
                'text/css/html-widget.css',
                '//fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic&subset=latin,latin-ext',
            )
        }
        js = (
            'text/bundle/medium-editor-3.0.0/js/medium-editor.min.js',
            'text/js/html-widget.js',
        )

    def __init__(self, attrs=None):
        default_attrs = {'cols': '40', 'rows': '10', 'class': 'djtext_editor_input', }
        if attrs:
            default_attrs.update(attrs)
        super(HTMLEditorWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        t = Text(type=Text.TYPE_HTML, body=value)
        rendered = t.render()
        return format_html(
            MARKDOWN_TEMPLATE,
            flatatt(final_attrs),
            force_text(value),
            rendered)
