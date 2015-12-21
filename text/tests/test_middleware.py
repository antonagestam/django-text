from django.test import TestCase
from django.http import HttpRequest
from django.template.base import Context, Template
from django.template.response import SimpleTemplateResponse
from django.utils.six import b

from mock import patch

from ..middleware import build_context, create_text, TextMiddleware, BackendTemplate, can_access_toolbar
from ..models import Text
from ..conf import settings


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
    def process_template_response(self, name, default=''):
        settings.TOOLBAR_INSTANT_UPDATE = False
        request = HttpRequest()
        context = Context({'request': request})
        node = Template(
            '{%% load text %%}{%% text "%s" "%s" %%}' % (name, default)).render(context)
        template = BackendTemplate(node)
        response = SimpleTemplateResponse(template, context)
        response.content = node
        mw = TextMiddleware()
        return mw.process_template_response(request, response).render()

    def test_default(self):
        content = "some test content"
        rendered = self.process_template_response('node', content)
        self.assertEqual(rendered.content, b(content))

    def test_db(self):
        text = Text(name='db_node', body='my awesome text', type=Text.TYPE_TEXT)
        text.save()
        rendered = self.process_template_response(text.name, default='this is the default')
        self.assertEqual(rendered.content, b(text.render()))


class TestAccessToolbar(TestCase):
    def test(self):
        class User(object):
            is_active = True
            is_staff = True

            def is_authenticated(self):
                return True

            def has_perm(self, perm):
                return True

        class InActiveUser(User):
            is_active = False

        class NotStaffUser(User):
            is_staff = False

        class NotAuthenticatedUser(User):
            def is_authenticated(self):
                return False

        class NoPermUser(User):
            def has_perm(self, perm):
                return False

        req = HttpRequest()
        req.user = User()

        settings.TOOLBAR_ENABLED = False
        self.assertFalse(can_access_toolbar(req))
        settings.TOOLBAR_ENABLED = True
        self.assertTrue(can_access_toolbar(req))
        req.user = InActiveUser()
        self.assertFalse(can_access_toolbar(req))
        req.user = NotStaffUser()
        self.assertFalse(can_access_toolbar(req))
        req.user = NotAuthenticatedUser()
        self.assertFalse(can_access_toolbar(req))
        req.user = NoPermUser()
        self.assertFalse(can_access_toolbar(req))
