from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        vaitro = request.POST.get('vaitro')
        if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
        else:
                User.objects.create_user(username=username, password=password, vaitro=vaitro)
                messages.success(request, 'Account created successfully')
                return redirect('login')

    return render(request, 'authentication-register1.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    # Clear any leftover messages from session
    from django.contrib.messages import get_messages
    storage = get_messages(request)
    storage.used = True
    request.session.pop('_messages', None)
    request.session.save()
    return render(request, 'authentication-login1.html')

def logout_view(request):
    from django.contrib.auth import logout
    from django.contrib import messages
    logout(request)
    # Clear any remaining messages from session
    from django.contrib.messages import get_messages
    storage = get_messages(request)
    storage.used = True
    request.session.pop('_messages', None)
    request.session.save()
    return redirect('login')


