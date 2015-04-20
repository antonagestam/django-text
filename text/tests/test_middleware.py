from django.test import TestCase
from django.http import HttpRequest
from django.template import Template, FilterExpression, Parser, Context
from django.template.response import SimpleTemplateResponse

from mock import patch

from text.middleware import build_context, create_text, TextMiddleware
from text.models import Text
from text.conf import settings
from text.templatetags.text import TextNode


class TestBuildContext(TestCase):
    def test_use_default(self):
        texts = []
        defaults = {'a_text_node': '<p>wooot</p>'}
        types = {'a_text_node': 'html'}
        c = build_context(texts, defaults, types)
        # test return value
        self.assertEqual(c['text_placeholder_a_text_node'], defaults['a_text_node'])
        # test model integration
        t = Text.objects.get(name='a_text_node')
        self.assertEqual(t.render(), defaults['a_text_node'])
        self.assertEqual(t.type, types['a_text_node'])

    @patch('text.middleware.create_text')
    def test_use_db(self, create_text):
        t = Text(name='my_text_node', type='markdown', body='# Hello')
        t.save()
        texts = [t]
        defaults = {'my_text_node': '<p>LOL</p>'}
        types = {'my_text_node': 'markdown'}
        c = build_context(texts, defaults, types)
        self.assertFalse(create_text.called)
        self.assertEqual(c['text_placeholder_my_text_node'], t.render())


class TestCreateText(TestCase):
    def test_use_default_type(self):
        name = 'my_text'
        body = 'my text is so awesome'
        t = create_text(name, body, None)
        self.assertEqual(t.type, Text.TYPE_TEXT)

    def test_save(self):
        name = 'my_text'
        body = 'my text is so awesome'
        text_type = 'html'
        settings.AUTOPOPULATE_TEXT = True
        t = create_text(name, body, text_type)
        tdb = Text.objects.get(name=name)
        self.assertEqual(t.type, text_type)
        self.assertEqual(tdb.type, text_type)
        self.assertEqual(t.name, name)
        self.assertEqual(tdb.name, name)
        self.assertEqual(t.body, body)
        self.assertEqual(tdb.body, body)

    def test_no_autopopulate(self):
        settings.AUTOPOPULATE_TEXT = False
        create_text('a_name', 'a body', Text.TYPE_HTML)
        self.assertEqual(Text.objects.count(), 0)


class TestTextMiddleware(TestCase):
    def fe(self, name):
        fe = FilterExpression('"{0}"'.format(name), Parser([]))
        return fe

    def process_template_response(self, name, default=''):
        settings.TOOLBAR_INSTANT_UPDATE = False
        request = HttpRequest()
        context = Context({'request': request})
        node = TextNode(self.fe(name), self.fe(default)).render(context)
        template = Template(node)
        response = SimpleTemplateResponse(template, context)
        response.content = node
        mw = TextMiddleware()
        return mw.process_template_response(request, response).render()

    def test_replace_with_default(self):
        content = "some test content"
        rendered = self.process_template_response('node', content)
        self.assertEqual(rendered.content, content)

    def test_replace_no_default(self):
        name = 'test_node'
        rendered = self.process_template_response(name)
        self.assertEqual(rendered.content, name)

    def test_replace_db(self):
        text = Text(name='db_node', body='my awesome text', type=Text.TYPE_TEXT)
        text.save()
        rendered = self.process_template_response(text.name, default='this is the default')
        self.assertEqual(rendered.content, text.render())
