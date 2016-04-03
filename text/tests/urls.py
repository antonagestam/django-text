from django.conf.urls import url, include

from text.urls import urlpatterns as django_text_patterns

urlpatterns = [
    url(r'^django_text/',
        include(django_text_patterns, namespace='django_text')),
]
