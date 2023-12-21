from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
import datetime


class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.CharField(unique= True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fav_categories = models.ManyToManyField('Category', blank=True)
    
    date_of_birth = models.DateField(blank=True, default=datetime.datetime.now)
    profile_pic = models.ImageField(upload_to="profile_pic/", default="profile_pic/default.png")
    

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save_profile(User, *args, **kwargs):
        User.save()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
   
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}: {self.content}'
