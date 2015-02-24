from sets import Set

from django import template

from ..models import Text

register = template.Library()


class TextGetter(object):
    def __init__(self):
        self.registered_texts = Set()
        self.texts = {}

    def register(self, text_name):
        self.registered_texts.add(text_name)

    def require(self, text_name):
        if text_name not in self.registered_texts:
            self.register(text_name)
        self.get_registered_texts()
        return self.texts[text_name]

    def get_registered_texts(self):
        texts = Text.objects.filter(name__in=self.registered_texts)
        for text in texts:
            self.texts[text.name] = text


text_getter = TextGetter()


class TextNode(template.Node):
    def __init__(self, text_name):
        self.text_name = text_name
        text_getter.register(text_name)

    def render(self, context):
        try:
            text = text_getter.require(self.text_name).render()
        except KeyError:
            text = self.text_name
        return text


@register.tag(name='editable')
def do_editable(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, text_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])

    return TextNode(text_name)
