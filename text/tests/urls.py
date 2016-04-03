from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin

from text.urls import urlpatterns as django_text_patterns

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='text/test_template.html'),
        name='django_text_test_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^django_text/',
        include(django_text_patterns, namespace='django_text')),
]
