from django import template

from text.models import text_getter

register = template.Library()


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
