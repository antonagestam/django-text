from django import forms
from django.utils.safestring import mark_safe
from django.template import Context, Template


class MarkdownEditorWidget(forms.widgets.Textarea):
    class Media:
        css = {
            'all': (
                'bundle/medium-editor-3.0.0/dist/css/medium-editor.min.css',
                'bundle/medium-editor-3.0.0/dist/css/themes/default.min.css',
            )
        }
        js = ('bundle/medium-editor-3.0.0/dist/js/medium-editor.min.js', )

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if 'class' not in attrs:
            attrs['class'] = ''
        attrs['class'] += ' editable'
        return super(MarkdownEditorWidget, self).render(name, value, attrs)
