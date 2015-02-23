from django import template

from ..models import Text

register = template.Library()


class TextNode(template.Node):
    def __init__(self, text_name):
        self.text_name = text_name

    def render(self, context):
        try:
            text = Text.objects.get(name=self.text_name)
        except Text.DoesNotExist:
            text = self.text_name
        return text.render()


@register.tag(name='editable')
def do_editable(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, text_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])

    return TextNode(text_name)
