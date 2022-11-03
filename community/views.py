from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .models import Post

def community(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'community/community.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request, 'community/post.html', context)