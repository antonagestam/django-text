from django.conf import settings as django_settings


class Conf:
    AUTOPOPULATE_TEXT = getattr(django_settings, 'AUTOPOPULATE_TEXT', True)
    TOOLBAR_FORM_PREFIX = getattr(django_settings, 'TEXT_TOOLBAR_FORM_PREFIX', 'djtext_form')
    TOOLBAR_ENABLED = getattr(django_settings, 'TEXT_TOOLBAR_ENABLED', True)

settings = Conf()
