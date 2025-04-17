from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserLoginForm, AccountEditForm


def index(request):
    return render(request, "news/home.html")

def account_view(request):
    return render(request, 'account.html', {
        'user': request.user
    })

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
    else:
        form = RegistrationForm()

    return render(request, 'news/register.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user =  authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('http://127.0.0.1:8000/')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})