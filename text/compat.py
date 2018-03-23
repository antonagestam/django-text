from django.template import Template, RequestContext, Context


def render_template(template, context=None, request=None):
    if isinstance(template, Template):
        if request:
            context = RequestContext(request, context)
        else:
            context = Context(context)
        return template.render(context)
    else:
        return template.render(context, request=request)
