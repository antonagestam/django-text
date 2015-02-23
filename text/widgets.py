from django import forms
from django.utils.safestring import mark_safe
from django.template import Context, Template


class MarkdownEditorWidget(forms.widgets.Textarea):
    class Media:
        css = {
            'all': (
                'text/bundle/medium-editor-3.0.0/css/medium-editor.min.css',
                'text/bundle/medium-editor-3.0.0/css/themes/default.min.css',
            )
        }
        js = (
            'text/bundle/medium-editor-3.0.0/js/medium-editor.min.js',
            'text/bundle/medium-editor-markdown-1.1.0/me-markdown.standalone.min.js',
        )

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if 'class' not in attrs:
            attrs['class'] = ''
        attrs['class'] += ' markdown'
        textarea = super(MarkdownEditorWidget, self).render(name, value, attrs)
        template = Template('text/markdown_editor_widget.html')
        context = Context({'textarea': textarea})
        return mark_safe(template.render(context))
