from django.test import TestCase
from django.template import FilterExpression, Parser
from django.http import HttpRequest

from text.templatetags.text import TextNode
from text.conf import settings


class TestTextNode(TestCase):
    def fe(self, name):
        fe = FilterExpression('"{0}"'.format(name), Parser([]))
        return fe

    def test_get_wrapped_placeholder(self):
        name = 'name_of_text_node'
        fe = self.fe(name)
        settings.TOOLBAR_INSTANT_UPDATE = True
        placeholder = TextNode(fe).get_placeholder({})
        expected = '<span data-text-name="name_of_text_node" class="dj_text_inline_wrapper">{{ text_placeholder_name_of_text_node }}</span>'
        self.assertEqual(placeholder, expected)

    def test_get_placeholder(self):
        name = 'name_of_text_node'
        fe = self.fe(name)
        settings.TOOLBAR_INSTANT_UPDATE = False
        placeholder = TextNode(fe).get_placeholder({})
        expected = '{{ text_placeholder_name_of_text_node }}'
        self.assertEqual(placeholder, expected)

    def test_set_default(self):
        name = 'name_of_text_node'
        content = 'test node content'
        context = {'request': HttpRequest()}
        fe = self.fe(name)
        t = TextNode(fe)
        t.set_default(name, context, content)
        self.assertEqual(context['request'].text_default_register[name], content)

    def test_set_type(self):
        name = 'name_of_text_node'
        type = 'html'
        context = {'request': HttpRequest()}
        fe = self.fe(name)
        t = TextNode(fe)
        t.set_type(name, context, type)
        self.assertEqual(context['request'].text_type_register[name], type)

    def test_register(self):
        name = 'name_of_text_node'
        context = {'request': HttpRequest()}
        fe = self.fe(name)
        t = TextNode(fe)
        t.register(name, context)
        self.assertIn(name, context['request'].text_register)

    def test_init_logic(self):
        name = self.fe('name_of_text_node')
        t = TextNode(name)
        self.assertEqual(t.text_name, t.default_text)
        default_text = self.fe('hejhej!')
        t = TextNode(name, default_text)
        self.assertEqual(t.default_text, default_text)
