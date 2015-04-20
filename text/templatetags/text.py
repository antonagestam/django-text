from django import template

from ..models import Text
from ..conf import settings

register = template.Library()


class TextNode(template.Node):
    def __init__(self, text_name, default_text='', text_type=Text.TYPE_TEXT):
        self.text_name = text_name
        if not isinstance(default_text, template.FilterExpression):
            default_text = template.FilterExpression(default_text, template.Parser([]))
        if default_text.token.replace('"', '').replace("'", '') == '' or not default_text:
            default_text = text_name
        self.default_text = default_text
        self.type = text_type
        if not isinstance(self.type, template.FilterExpression):
            self.type = template.FilterExpression(self.type, template.Parser([]))

    def resolved_text_name(self, context):
        text_name = self.text_name.resolve(context)
        if not text_name or text_name.strip() == '':
            raise template.TemplateSyntaxError("Invalid text node name")
        return text_name

    def set_default(self, text_name, context, content):
        if not hasattr(context['request'], 'text_default_register'):
            context['request'].text_default_register = {}
        context['request'].text_default_register[text_name] = content.strip()

    def set_type(self, text_name, context, text_type):
        if not hasattr(context['request'], 'text_type_register'):
            context['request'].text_type_register = {}
        context['request'].text_type_register[text_name] = text_type

    def register(self, text_name, context):
        if not hasattr(context['request'], 'text_register'):
            context['request'].text_register = []
        context['request'].text_register.append(text_name)

    def get_placeholder(self, context):
        placeholder = "{{ text_placeholder_%s }}"
        text_name = self.resolved_text_name(context)
        if settings.TOOLBAR_INSTANT_UPDATE:
            before, after = settings.INLINE_WRAPPER
            before = before.format(text_name, settings.INLINE_WRAPPER_CLASS)
            placeholder = ''.join((before, placeholder, after))
        return placeholder % text_name

    def render(self, context):
        text_name = self.resolved_text_name(context)
        self.register(text_name, context)
        self.set_default(text_name, context, self.default_text.resolve(context))
        self.set_type(text_name, context, self.type.resolve(context))
        return self.get_placeholder(context)


class BlockTextNode(TextNode):
    def __init__(self, nodelist, *args, **kwargs):
        super(BlockTextNode, self).__init__(*args, **kwargs)
        self.nodelist = nodelist

    def render(self, context):
        text_name = self.resolved_text_name(context)
        self.register(text_name, context)
        self.set_default(text_name, context, self.nodelist.render(context))
        self.set_type(text_name, context, self.type.resolve(context))
        return self.get_placeholder(context)


@register.tag(name='text')
def text(parser, token):
    bits = token.split_contents()
    text_name = bits[1]
    try:
        default = bits[2]
        text_type = bits[3]
    except IndexError:
        default = text_name
        text_type = Text.TYPE_TEXT
    default = parser.compile_filter(default)
    text_name = parser.compile_filter(text_name)
    text_type = parser.compile_filter(text_type)
    return TextNode(text_name, default, text_type)


@register.tag(name='blocktext')
def blocktext(parser, token):
    nodelist = parser.parse(('endblocktext', ))
    parser.delete_first_token()
    bits = token.split_contents()
    text_name = parser.compile_filter(bits[1])
    try:
        text_type = bits[2]
    except IndexError:
        text_type = Text.TYPE_TEXT
    text_type = parser.compile_filter(text_type)
    return BlockTextNode(nodelist, text_name, text_type=text_type)
