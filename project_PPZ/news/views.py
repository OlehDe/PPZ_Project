from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, UserLoginForm, AccountEditForm, NewsForm

from django.contrib.auth.decorators import login_required
from .models import News

def home(request):
    news_list = News.objects.all().order_by('-created_at')
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

        News.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user
        )
        return redirect('http://127.0.0.1:8000/')
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


@login_required
def edit_news(request):
    news = News.objects.filter(author=request.user).first()  # Отримуємо першу новину, що належить користувачеві
    if not news:
        return HttpResponseForbidden("У вас немає новин для редагування.")

    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        image = request.FILES.get('image')
        if image:
            news.image = image
        news.save()
        return redirect('http://127.0.0.1:8000/')

    return render(request, 'news/edit_news.html', {'news': news})

@login_required
def delete_news(request):
    news = News.objects.filter(author=request.user).first()
    if request.user != news.author:
        return HttpResponseForbidden("Ви не можете видалити цю новину.")

    if request.method == 'POST':
        news.delete()
        return redirect('http://127.0.0.1:8000/')

    return render(request, 'news/delete_confirm.html', {'news': news})
