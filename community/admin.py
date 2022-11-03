from django.contrib import admin

from .models import Post, Topic, Message

# Register your models here.
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Message)