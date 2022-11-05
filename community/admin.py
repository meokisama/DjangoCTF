from django.contrib import admin

from .models import Post, Topic, Comment, User

# Register your models here.
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(User)