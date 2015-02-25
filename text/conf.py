from django.conf import django_settings


class Conf:
    AUTOPOPULATE_TEXT = getattr(settings, 'AUTOPOPULATE_TEXT', False)


settings = Conf()
