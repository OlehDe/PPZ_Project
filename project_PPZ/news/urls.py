from django.urls import path, include
from django.contrib import admin
from . import views
from .views import register_view, login_view, account_view

app_name = "news"
urlpatterns = [
    path('', views.index, name='index'),
    path('', views.account_view, name='account'),
    path('account', account_view, name='account'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
]
