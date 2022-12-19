from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="static/main/images/avatar.svg")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
        return self.title



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(editable=True)
    content = models.TextField()
    challenge_id=models.IntegerField(null=True,blank=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.content