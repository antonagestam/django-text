from django.conf import settings as django_settings


class Conf(object):
    AUTOPOPULATE_TEXT = getattr(django_settings, 'AUTOPOPULATE_TEXT', True)
    TOOLBAR_FORM_PREFIX = getattr(django_settings, 'TEXT_TOOLBAR_FORM_PREFIX', 'djtext_form')
    TOOLBAR_ENABLED = getattr(django_settings, 'TEXT_TOOLBAR_ENABLED', True)
    TOOLBAR_INSTANT_UPDATE = getattr(django_settings, 'TEXT_TOOLBAR_INSTANT_UPDATE', True)
    INLINE_WRAPPER = getattr(django_settings, 'TEXT_INLINE_WRAPPER', (
        '<span data-text-name="{0}" class="{1}">', '</span>'))
    INLINE_WRAPPER_CLASS = getattr(django_settings, 'TEXT_INLINE_WRAPPER_CLASS', 'dj_text_inline_wrapper')

settings = Conf()
