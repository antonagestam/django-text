from django.template.response import SimpleTemplateResponse
from django.template import Template, Context
from django.utils.translation import get_language

from .conf import settings
from .models import text_setter, Text

from logging import getLogger
l = getLogger(__name__)


def build_context(texts, defaults):
    placeholder = "text_placeholder_{0}"
    context = {placeholder.format(t.name): t.render for t in texts}
    for name, text in defaults.iteritems():
        name = placeholder.format(name)
        if name not in context:
            context[name] = text
            text_setter.set(name, text)
    return context


class TextMiddleware(object):
    def process_response(self, request, response):
        if settings.AUTOPOPULATE_TEXT:
            text_setter.save()
        return response

    def process_request(self, request):
        text_setter.clear()

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
        l.debug({t.name: t.render() for t in texts})
        return SimpleTemplateResponse(template, context)
