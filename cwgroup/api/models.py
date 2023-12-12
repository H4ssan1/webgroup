from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
import datetime


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.CharField(unique= True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
    date_of_birth = models.DateField(blank=True, default=datetime.datetime.now)
    profile_pic = models.ImageField(upload_to="profile_pic/")
    

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save_profile(User, *args, **kwargs):
        User.save()
