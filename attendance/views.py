from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm
from .models import User

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')

def dashboard(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'dashboard.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User Created Successfully')
            return redirect('dashboard')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
