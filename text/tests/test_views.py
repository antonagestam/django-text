from django.test import TestCase, RequestFactory
from django.http import Http404
from django.contrib.auth.models import User

from text.views import Slug, TextView
from text.models import Text


class TestTextView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/text/a_text_node_en-us/')
        self.request.user = User.objects.create_user(
            'admin', 'admin@example.com', 'password')
        self.view = TextView.as_view()
        self.text = Text(
            name='a_text_node',
            body='hello',
            type=Text.TYPE_TEXT,
            language='en-us')

    def test_parse_slug(self):
        s = TextView.parse_slug('the_node_name_sv-se')
        self.assertIsInstance(s, Slug)
        self.assertEqual(s.language, 'sv-se')
        self.assertEqual(s.name, 'the_node_name')

        with self.assertRaises(Http404):
            TextView.parse_slug('the')

    def test_get(self):
        self.text.save()
        with self.assertRaises(Http404):
            self.view(self.request)

        self.request.user.is_staff = True
        self.request.user.is_superuser = True
        response = self.view(self.request, text_slug='a_text_node_en-us')
        self.assertEqual(response.status_code, 200)
