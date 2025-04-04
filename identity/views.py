from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from base.views import index_view

from identity.forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(index_view)
            else:
                messages.error(request, 'Username or password is incorrect')
        return render(request, 'identity/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'identity/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(reverse("identity:login"))