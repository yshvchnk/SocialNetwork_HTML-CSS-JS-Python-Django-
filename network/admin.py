from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, NewPost, Like, Follow

admin.site.register(User, UserAdmin)
admin.site.register(NewPost)
admin.site.register(Like)
admin.site.register(Follow)