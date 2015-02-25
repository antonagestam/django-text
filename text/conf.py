from django.conf import settings as django_settings


class Conf:
    AUTOPOPULATE_TEXT = getattr(django_settings, 'AUTOPOPULATE_TEXT', True)


settings = Conf()
