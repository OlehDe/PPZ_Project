from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect

from .forms import RegistrationForm, UserLoginForm, AccountEditForm, NewsForm, CommentForm

from django.contrib.auth.decorators import login_required
from .models import News, Comment

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponse("У вас немає прав для видалення цього коментаря.")
    news_id = comment.news.pk
    comment.delete()
    return redirect('news:news_detail', pk=news_id)

@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if news.author != request.user:
        return HttpResponse("У вас немає прав для видалення цієї новини.")
    news.delete()
    return redirect('news:news_list')

@login_required
def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if news.author != request.user:
        return HttpResponse("У вас немає прав для редагування цієї новини.")
    form = NewsForm(request.POST or None, request.FILES or None, instance=news)
    if form.is_valid():
        form.save()
        return redirect('news:news_list')
    return render(request, 'news/news_form.html', {'form': form})

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news:news_list')
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.all().order_by('-created_at')
    form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.news = news
                comment.author = request.user
                comment.save()
                return redirect('news:news_detail', pk=news.pk)
        else:
            form = CommentForm()

    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form
    })

def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_list': news_list})

def index(request):
    return render(request, "news/home.html")

def account_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # зберігаємо користувача
            return redirect('http://127.0.0.1:8000/')  # або використай reverse('home')
    else:
        form = RegistrationForm()  # створення нової форми при GET-запиті

    return render(request, 'news/account.html', {
        'form': form,
        'user': request.user
    })


# def register_view(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('http://127.0.0.1:8000/')
#     else:
#         form = RegistrationForm()
#
#     return render(request, 'news/register.html', {"form": form})
#
# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user =  authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('http://127.0.0.1:8000/')
#     else:
#         form = UserLoginForm()
#     return render(request, 'news/login.html', {'form': form})
#
# def logout_view(request):
#     logout(request)
#     return redirect('http://127.0.0.1:8000/')