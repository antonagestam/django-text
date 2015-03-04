from django.template.response import SimpleTemplateResponse
from django.template import Template, Context
from django.utils.translation import get_language

from .conf import settings
from .models import Text


def build_context(texts, defaults, types):
    placeholder = "text_placeholder_{0}"
    context = {placeholder.format(t.name): t.render() for t in texts}
    for name, text in defaults.iteritems():
        pname = placeholder.format(name)
        if pname not in context:
            context[pname] = create_text(name, text, types[name]).render()
    return context


def create_text(name, text, type):
    language = get_language()
    text = Text(
        name=name,
        body=text,
        language=language,
        type=type)
    if settings.AUTOPOPULATE_TEXT:
        text.save()
    return text


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
        if hasattr(request, 'text_type_register'):
            types = request.text_type_register
        else:
            types = {}
        context = Context(build_context(texts, defaults, types))
        return SimpleTemplateResponse(template, context)
