from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    email = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(default="default.png", upload_to="profile_pic/")

    def __str__(self):
        return f"{self.id}:{self.username} {self.email}"