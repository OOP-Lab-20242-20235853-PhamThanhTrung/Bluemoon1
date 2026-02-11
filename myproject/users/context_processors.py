from django.contrib.messages.api import get_messages

def messages(request):
    """
    Return messages for the request, but clear them for login/register pages.
    """
    if request.path in ['/login/', '/register/'] and request.method == 'GET':
        # For login/register pages, return empty messages and mark as used
        storage = get_messages(request)
        storage.used = True
        return {'messages': []}
    else:
        return {'messages': get_messages(request)}