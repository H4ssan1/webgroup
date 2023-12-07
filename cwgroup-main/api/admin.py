from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class UserAdminclass(UserAdmin):
    list_display = ("email",)




admin.site.register(User, UserAdminclass)