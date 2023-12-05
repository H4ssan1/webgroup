from django.contrib.auth.models import AbstractUser
from django.db import models

#Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=200, unique= True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    #admin function
    def str(self):
        return f'{self.email} Profile'