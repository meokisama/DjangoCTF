from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from .models import Post, Topic
from .forms import PostForm

def community(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    post_count = posts.count()
    context = {'posts':posts, 'topics':topics, 'post_count':post_count}
    return render(request, 'community/community.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request, 'community/post.html', context)

def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community')
    context = {'form':form}
    return render(request, 'community/post_form.html', context)

def updatePost(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community')
    context = {'form':form}
    return render(request, 'community/post_form.html', context)

def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('community')
    return render(request, 'community/delete.html', {'obj':post})