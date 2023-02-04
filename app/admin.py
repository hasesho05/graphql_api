from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User, Post


class PostCustom(ModelAdmin):
    list_desplay = ("channel_name", "caption", "created_at")
    list_desplay_links = "channel_name"
    ordering = ("-created_at",)


admin.site.register(Post, PostCustom)
admin.site.register(User)
