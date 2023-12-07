from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})



def profile(request, profile_id):
    profile = CustomUser.objects.get(pk=profile_id)
    return render(request, 'api/profile.html', {
        "profile": profile,
    })