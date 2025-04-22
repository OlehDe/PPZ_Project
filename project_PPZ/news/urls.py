from django.urls import path, include
from django.contrib import admin
from . import views
from .views import register_view, login_view, account_view, logout_view

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserLoginForm, AccountEditForm

app_name = "news"

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.account_view, name='account'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
]
