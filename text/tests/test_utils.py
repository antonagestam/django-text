from django.test import TestCase
from django.http import HttpRequest

from ..conf import settings
from ..utils import access_toolbar


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


class TestAccessToolbar(TestCase):
    def test(self):
        req = HttpRequest()
        req.user = User()

        settings.TOOLBAR_ENABLED = False
        self.assertFalse(access_toolbar(req))
        settings.TOOLBAR_ENABLED = True
        self.assertTrue(access_toolbar(req))
        req.user = InActiveUser()
        self.assertFalse(access_toolbar(req))
        req.user = NotStaffUser()
        self.assertFalse(access_toolbar(req))
        req.user = NotAuthenticatedUser()
        self.assertFalse(access_toolbar(req))
        req.user = NoPermUser()
        self.assertFalse(access_toolbar(req))
