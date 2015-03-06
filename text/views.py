from django.http import JsonResponse, Http404, HttpResponse
from django.views.generic import DetailView, UpdateView

from .models import Text
from .forms import TextForm
from .conf import settings
from .utils import access_toolbar


class TextView(DetailView):
    model = Text

    def get_object(self, queryset=None):
        slug = self.kwargs.get('text_slug', None)
        parts = slug.split('_')
        language = parts[-1]
        name = '_'.join(parts[:-1])
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(name=name, language=language)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("Found no text with that id")
        return obj

    def get(self, request, *args, **kwargs):
        if not access_toolbar(request):
            raise Http404()
        self.object = self.get_object()
        data = {
            'id': self.object.id,
            'body': self.object.body,
            'type': self.object.type,
            'language': self.object.language,
            'render': self.object.render(),
            'name': self.object.name,
        }
        return JsonResponse(data=data)


class TextUpdateView(UpdateView):
    model = Text
    form_class = TextForm
    pk_url_kwarg = 'text_id'
    form_prefix = settings.TOOLBAR_FORM_PREFIX

    def get_form_kwargs(self):
        kwargs = super(TextUpdateView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def post(self, request, *args, **kwargs):
        if not access_toolbar(request):
            raise Http404()
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({'errors': form.errors, 'success': False})
