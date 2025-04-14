from django.urls import path
from . import views
from .views import register_view, login_view

app_name = "news"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
]
