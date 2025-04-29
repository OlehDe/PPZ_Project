from django.conf.urls.static import static
from django.urls import path

from . import views

from .views import register_view, login_view, comment_delete, news_comments, user_comments


app_name = "news"

urlpatterns = [
    path('news/', views.news_list, name='news_list'),

    path('', views.home, name='home'),
    path('edit_news', views.edit_news, name='edit_news'),
    path('delete_news', views.delete_news, name='delete_news'),
    path('add_news/', views.add_news, name='add_news'),
    path('account', views.account_view, name='account'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comments/<int:news_id>/', views.news_comments, name='news_comments'),
    path('user_comments/', views.user_comments, name='user_comments'),

    path('comments/<int:news_id>/add/', views.add_comment, name='add_comment'),
]

