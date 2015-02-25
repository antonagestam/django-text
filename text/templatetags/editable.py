from django import template

from text.models import text_getter, text_setter
from text.conf import settings

register = template.Library()


class TextNode(template.Node):
    def __init__(self, text_name):
        self.text_name = text_name
        text_getter.register(text_name)

    def set_missing(self, text):
        if settings.AUTOPOPULATE_TEXT:
            text_setter.set(self.text_name, text)

    def render(self, context):
        try:
            text = text_getter.require(self.text_name).render()
        except KeyError:
            text = self.text_name
            self.set_missing(text)
        return text


class BlockTextNode(TextNode):
    def __init__(self, nodelist, *args, **kwargs):
        super(BlockTextNode, self).__init__(*args, **kwargs)
        self.nodelist = nodelist

    def render(self, context):
        try:
            text = text_getter.require(self.text_name).render()
        except KeyError:
            text = self.nodelist.render(context)
            self.set_missing(text)
        return text


def get_text_name(token):
    try:
        # split_contents() knows not to split quoted strings.
        __, text_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    return text_name

@register.tag(name='editable')
def editable(parser, token):
    return TextNode(get_text_name(token))


@register.tag(name='blockeditable')
def blockeditable(parser, token):
    nodelist = parser.parse(('endblockeditable', ))
    parser.delete_first_token()
    return BlockTextNode(nodelist, get_text_name(token))
