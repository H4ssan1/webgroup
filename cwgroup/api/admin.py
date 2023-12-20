from django.contrib import admin



#from django.contrib.auth.admin import UserAdmin
from .models import Profile, User, NewsArticle, Category, Comment


admin.site.register(Profile)
admin.site.register(User)
admin.site.register(NewsArticle)
admin.site.register(Category)
admin.site.register(Comment)