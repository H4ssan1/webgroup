"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from .views import main_spa, home
from .views import MyLoginView, RegisterView, MyProfile #, profile

from . import views

from django.contrib.auth.views import (
    LogoutView, 
)


urlpatterns = [
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('profile_backend/', MyProfile.as_view(), name='profile'),
    path('home/', home, name='home'),
    path('',views.serve_vue_app, name='serve_vue_app'),
    path('user_data/',views.user_details, name='user_details'),
    path('articles/', views.list_news_articles, name='articles'),
    path('article/<int:article_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('article/<int:article_id>/comments/', views.get_comment, name='get_comments'),
    path('update_user_profilePic/', views.update_profile_pic, name='update_profile_pic'),
    path('update_user/', views.updateUser, name='update_user'),
    path('update_fav_categories/', views.update_fav_categories, name='update_fav_categories'),
]
