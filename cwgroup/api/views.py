import json
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, get_object_or_404
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
        
        'date_of_birth': user.profile.date_of_birth,  
        'profile_image': user.profile.profile_pic.url if user.profile.profile_pic else None,  
        'id' : user.profile.id,
        
    }
    return JsonResponse(data)

def list_news_articles(request):
    articles = NewsArticle.objects.all().values('id', 'title', 'content', 'category__name')
    return JsonResponse(list(articles), safe=False)


@login_required
@csrf_exempt
def add_comment(request, article_id):
    article = get_object_or_404(NewsArticle, pk=article_id)

   
    data = json.loads(request.body)
    content = data.get('content')
    parent_id = data.get('parent_id')

    parent_comment = None
    if parent_id:
        parent_comment = get_object_or_404(Comment, pk=parent_id)

    comment = Comment.objects.create(
        article=article, 
        user=request.user, 
        content=content,
        parent=parent_comment
    )

    return JsonResponse({'message': 'Comment added successfully', 'comment_id': comment.id})

@login_required
@csrf_exempt
def edit_comment(request, comment_id):
    try:
        data = json.loads(request.body)
        content = data.get('content')
        if not content:
            return HttpResponseBadRequest('Content is required.')

        comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
        comment.content = content
        comment.save()
        return JsonResponse({'message': 'Comment updated successfully'})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

@login_required
@csrf_exempt
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'message': 'Comment deleted successfully'})

@login_required
def get_comment(request, article_id):
    article = get_object_or_404(NewsArticle, pk=article_id)

    comments = Comment.objects.filter(article=article).order_by('-created_at')  

    comments_data = [{
        'id': comment.id,
        'user': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'parent_id': comment.parent.id if comment.parent else None
    } for comment in comments]

    return JsonResponse(comments_data, safe=False)




@login_required
@csrf_exempt
def updateUser(request):
    user = request.user
    profile = user.profile
    data = json.loads(request.body)
    user.email = data['email']
    profile.date_of_birth = data['date_of_birth']
    user.save()
    profile.save()
    return JsonResponse({'status': 'success'})

@login_required
@csrf_exempt
def update_profile_pic(request):
    

    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)

    profile_pic = request.FILES.get('profile_pic')
    if not profile_pic:
        return JsonResponse({'error': 'No image provided'}, status=400)

    profile.profile_pic = profile_pic
    profile.save()
    return JsonResponse({'message': 'Profile picture updated successfully'}, status=200)
