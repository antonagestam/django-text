from django.conf.urls import patterns, url

from .views import TextView, TextUpdateView


urlpatterns = patterns(
    '',
    url(r'^text/(?P<text_slug>\w+)/$', TextView.as_view(), name='text'),
    url(r'^update_text/(?P<text_id>\d+)/$', TextUpdateView.as_view(), name='update_text'),
)
