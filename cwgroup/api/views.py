from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from .models import User, Profile, NewsArticle
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from django.shortcuts import render, redirect
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views import View

import os
from django.conf import settings


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

class RegisterView(FormView):
    template_name = 'api/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('serve_vue_app')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            
        return super(RegisterView, self).form_valid(form)
    
    
class MyLoginView(LoginView):
    template_name = 'api/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('serve_vue_app') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'api/profile.html', context)
    
    def post(self, request):
        user_form = UserUpdateForm(
            request.POST,
            instance = request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance = request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully')

            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request, 'Error updating profile')

            return render(request, 'api/profile.html', context)
        
def home(request):
    return render(request,'home.html')


@login_required
def serve_vue_app(request):
        # This path should be to the 'index.html' inside your 'api/static/api/spa' directory.
        index_file_path = os.path.join(settings.BASE_DIR, 'api', 'static', 'api', 'spa', 'index.html')
        try:
            with open(index_file_path, 'r') as file:
                return HttpResponse(file.read(), content_type='text/html')
        except FileNotFoundError:
            return HttpResponse(
                "The Vue.js app was not found. Have you run 'npm run build'?",
                status=404
            )
        

@login_required
def user_details(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        # Add additional fields as necessary
        'date_of_birth': user.profile.date_of_birth,  # Assuming date_of_birth is a field on Profile
        'profile_image': user.profile.profile_pic.url if user.profile.profile_pic else None,  # Assuming profile_image is a ImageField on Profile
        
    }
    return JsonResponse(data)

def list_news_articles(request):
    articles = NewsArticle.objects.all().values('id', 'title', 'content', 'category__name')
    return JsonResponse(list(articles), safe=False)