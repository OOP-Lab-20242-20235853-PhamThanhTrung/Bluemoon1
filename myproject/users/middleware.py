from django.contrib.messages import get_messages

class ClearMessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear messages for login page
        if request.path == '/login/' and request.method == 'GET':
            storage = get_messages(request)
            storage.used = True
            request.session.pop('_messages', None)
        response = self.get_response(request)
        return response