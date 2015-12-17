from django import template

from ..models import Text
from ..conf import settings

register = template.Library()


def get_placeholder(node_name, context):
    placeholder = "{{ text_placeholder_%s }}"
    if settings.TOOLBAR_INSTANT_UPDATE:
        before, after = settings.INLINE_WRAPPER
        before = before.format(node_name, settings.INLINE_WRAPPER_CLASS)
        placeholder = ''.join((before, placeholder, after))
    return placeholder % node_name


def set_default(node_name, context, content):
    if not hasattr(context['request'], 'text_default_register'):
        context['request'].text_default_register = {}
    context['request'].text_default_register[node_name] = content.strip()


def set_type(node_name, context, text_type):
    if not hasattr(context['request'], 'text_type_register'):
        context['request'].text_type_register = {}
    context['request'].text_type_register[node_name] = text_type


def register_node(node_name, context):
    if not hasattr(context['request'], 'text_register'):
        context['request'].text_register = []
    context['request'].text_register.append(node_name)


def resolve_args(spec, args, context):
    resolved_args = {}

    if len(args) - 1 > len(spec['params']):
        raise template.TemplateSyntaxError('%s tag received too many arguments' % args[0])

    for i, arg in enumerate(spec['params'], start=1):
        # Try assigning the input bit
        try:
            val = args[i]
        except IndexError:
            # Raise an error if the argument is required
            if arg not in spec['defaults']:
                raise template.TemplateSyntaxError('%s tag received too many arguments' % args[0])
            # Assign default value
            resolved_args[arg] = spec['defaults'][arg]

        if not (val[0] == val[-1] and val[0] in ('"', "'")):
            # The input is not quoted, treat as a variable
            try:
                resolved_args[arg] = template.Variable(val).resolve(context)
            except template.VariableDoesNotExist:
                raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % args[0])
        else:
            # The input is a quoted string
            resolved_args[arg] = val[1:-1]
    return resolved_args


class TextNode(template.Node):
    spec = {
        'params': ('node_name', 'default_text', 'node_type'),
        'defaults': {
            'node_type': Text.TYPE_TEXT,
        },
    }

    def __init__(self, args):
        self.args = args

    def render(self, context):
        resolved_args = resolve_args(self.spec, self.args, context)
        node_name = resolved_args['node_name']
        default_text = resolved_args['default_text']
        node_type = resolved_args['node_type']
        print("NODE TYPE:", node_type)
        register_node(node_name, context)
        set_default(node_name, context, default_text)
        set_type(node_name, context, node_type)
        return get_placeholder(node_name, context)


class BlockTextNode(TextNode):
    spec = {
        'params': ('node_name', 'node_type'),
        'defaults': {
            'node_type': Text.TYPE_HTML,
        },
    }

    def __init__(self, args, default_text):
        super(BlockTextNode, self).__init__(args)
        self.default_text = default_text

    def render(self, context):
        resolved_args = resolve_args(self.spec, self.args, context)
        node_name = resolved_args['node_name']
        node_type = resolved_args['node_type']
        register_node(node_name, context)
        set_default(node_name, context, self.default_text)
        set_type(node_name, context, node_type)
        return get_placeholder(node_name, context)


@register.tag(name='text')
def text(parser, token):
    """ Syntax: {% text <node_name> <default_text> <node_type> %} """
    bits = token.split_contents()
    return TextNode(bits)


@register.tag(name='blocktext')
def blocktext(parser, token):
    """ Syntax: {% blocktext <node_name> <node_type> %}<default_text>{% endblocktext %} """
    nodelist = parser.parse(('endblocktext', ))
    parser.delete_first_token()
    bits = token.split_contents()
    return BlockTextNode(bits, nodelist)
