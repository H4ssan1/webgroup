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
    #path('', main_spa),
    path('profile_backend/', MyProfile.as_view(), name='profile'),
    #path('profile/update/', post_save, name='update'),
    path('home/', home, name='home'),
    path('',views.serve_vue_app, name='serve_vue_app'),
    path('user_data/',views.user_details, name='user_details'),
    
]
