from django import template

import markdown

from ..models import Text

register = template.Library()


class TextNode(template.Node):
    def __init__(self, text_name):
        self.text_name = text_name

    def render(self, context):
        try:
            text = Text.objects.get(name=self.text_name).body
        except Text.DoesNotExist:
            text = self.text_name
        return markdown.markdown(text, output_format='html5')


@register.tag(name='editable')
def do_editable(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, text_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])

    return TextNode(text_name)
