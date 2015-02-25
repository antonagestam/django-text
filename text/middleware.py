from text.models import text_setter


class AutoPopulateMiddleware(object):
    def process_response(self, request, response):
        text_setter.save()
        return response

    def process_request(self, request):
        text_setter.clear()
