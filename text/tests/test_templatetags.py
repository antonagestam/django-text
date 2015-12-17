from django.test import TestCase
from django.http import HttpRequest
from django.template import Template, Context

from text.templatetags.text import set_default, set_type, register_node, get_placeholder
from text.conf import settings


load_statement = "{% load text %}"

class TestTextTag(TestCase):
    def get_context(self):
        return Context({'request': HttpRequest()})

    def test_variable(self):
        settings.TOOLBAR_INSTANT_UPDATE = False
        context = self.get_context()
        node_name = 'a_node'
        default_text = 'some default content :)'
        text_type = "html"
        template = Template(load_statement + """\
{%% with t="%s" %%}{%% text "%s" t "%s" %%}{%% endwith %%}""" % (default_text, node_name, text_type))
        output = template.render(context)
        self.assertEqual(output, '{{ text_placeholder_%s }}' % node_name)
        self.assertEqual(context['request'].text_default_register[node_name], default_text)
        self.assertEqual(context['request'].text_type_register[node_name], text_type)
        self.assertIn(node_name, context['request'].text_register)

    def test_without_node_type(self):
        settings.TOOLBAR_INSTANT_UPDATE = False
        context = self.get_context()
        node_name = 'a_node'
        default_text = 'this is my default text'
        template = Template(load_statement + '{%% text "%s" "%s" %%}' % (node_name, default_text))
        output = template.render(context)
        self.assertEqual(output, '{{ text_placeholder_%s }}' % node_name)
        self.assertEqual(context['request'].text_default_register[node_name], default_text)
        self.assertEqual(context['request'].text_type_register[node_name], "text")
        self.assertIn(node_name, context['request'].text_register)


class TestBlockTextTag(TestCase):
    pass


class TestGetPlaceholder(TestCase):
    def test_get_wrapped_placeholder(self):
        name = 'name_of_text_node'
        settings.TOOLBAR_INSTANT_UPDATE = True
        placeholder = get_placeholder(name, {})
        expected = '<span data-text-name="name_of_text_node" class="dj_text_inline_wrapper">{{ text_placeholder_name_of_text_node }}</span>'
        self.assertEqual(placeholder, expected)

    def test_get_placeholder(self):
        name = 'name_of_text_node'
        settings.TOOLBAR_INSTANT_UPDATE = False
        placeholder = get_placeholder(name, {})
        expected = '{{ text_placeholder_name_of_text_node }}'
        self.assertEqual(placeholder, expected)


class TestSetDefault(TestCase):
    def test_set_default(self):
        name = 'name_of_text_node'
        content = 'test node content'
        context = {'request': HttpRequest()}
        set_default(name, context, content)
        self.assertEqual(context['request'].text_default_register[name], content)


class TestSetType(TestCase):
    def test_set_type(self):
        name = 'name_of_text_node'
        text_type = 'html'
        context = {'request': HttpRequest()}
        set_type(name, context, text_type)
        self.assertEqual(context['request'].text_type_register[name], text_type)


class TestRegister(TestCase):
    def test_register(self):
        name = 'name_of_text_node'
        context = {'request': HttpRequest()}
        register_node(name, context)
        self.assertIn(name, context['request'].text_register)
