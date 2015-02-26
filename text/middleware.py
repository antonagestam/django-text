from django.template.response import SimpleTemplateResponse
from django.template import Template, Context
from django.utils.translation import get_language

from .conf import settings
from .models import Text


def build_context(texts, defaults):
    placeholder = "text_placeholder_{0}"
    context = {placeholder.format(t.name): t.render() for t in texts}
    for name, text in defaults.iteritems():
        pname = placeholder.format(name)
        if pname not in context:
            context[pname] = text
            populate_text(name, text)
    return context


def populate_text(name, text):
    if not settings.AUTOPOPULATE_TEXT:
        return
    language = get_language()
    text = Text(
        name=name,
        body=text,
        language=language,
        type=Text.TYPE_TEXT)
    text.save()


class TextMiddleware(object):
    def process_template_response(self, request, response):
        template = Template(response.render().content)
        if not hasattr(request, 'text_register'):
            return response
        language = get_language()
        texts = Text.objects.filter(
            name__in=request.text_register,
            language=language)
        if hasattr(request, 'text_default_register'):
            defaults = request.text_default_register
        else:
            defaults = {}
        context = Context(build_context(texts, defaults))
        return SimpleTemplateResponse(template, context)
