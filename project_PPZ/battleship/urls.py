# project_PPZ/battleship/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attack/', views.attack, name='attack'),
    path('reset/', views.reset_game, name='reset_game'),
]
