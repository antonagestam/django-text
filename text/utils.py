from .conf import settings


def access_toolbar(request):
    if not settings.TOOLBAR_ENABLED:
        return False
    user = request.user
    return (user.is_authenticated() and user.is_active and user.is_staff and
            user.has_perm('text.change_text'))
