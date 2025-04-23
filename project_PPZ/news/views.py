from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserLoginForm, AccountEditForm, NewsForm

from django.contrib.auth.decorators import login_required
from .models import News

def home(request):
    news_list = News.objects.all().order_by('created_at')
    return render(request, 'news/home.html', {'news_list': news_list})

def news_list(request):
    news = News.objects.all().order_by('-created_date')
    return render(request, 'news/news_list.html', {'news': news})


@login_required
def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        news = News.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user
        )
        return redirect('news_list')
    return render(request, 'news/add_news.html')


def index(request):
    return render(request, "news/home.html")

def account_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # зберігаємо користувача
            return redirect('http://127.0.0.1:8000/')
    else:
        form = RegistrationForm()

    return render(request, 'news/account.html', {
        'form': form,
        'user': request.user
    })

def account(request):
    return render(request, 'account.html')


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

def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')