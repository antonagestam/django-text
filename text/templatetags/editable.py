from django import template

register = template.Library()

from logging import getLogger
l = getLogger(__name__)


class TextNode(template.Node):
    def __init__(self, text_name):
        self.text_name = text_name

    def set_default(self, context, content):
        if not hasattr(context['request'], 'text_default_register'):
            context['request'].text_default_register = {}
        context['request'].text_default_register[self.text_name] = content

    def register(self, context):
        if not hasattr(context['request'], 'text_register'):
            context['request'].text_register = []
        context['request'].text_register.append(self.text_name)

    def get_placeholder(self):
        return "{{ text_placeholder_%s }}" % self.text_name

    def render(self, context):
        self.register(context)
        self.set_default(context, self.text_name)
        return self.get_placeholder()


class BlockTextNode(TextNode):
    def __init__(self, nodelist, *args, **kwargs):
        super(BlockTextNode, self).__init__(*args, **kwargs)
        self.nodelist = nodelist

    def render(self, context):
        self.register(context)
        self.set_default(context, self.nodelist.render(context))
        return self.get_placeholder()


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
