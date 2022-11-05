from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Post, Topic, Comment, User
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
    comments = Comment.objects.filter(Q(post__topic__name__icontains=q))

    context = {'posts':posts, 'topics':topics, 'post_count':post_count,'comments':comments}
    return render(request, 'community/community.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comment_set.all().order_by('-created')
    participants = post.participants.all()
    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            post = post,
            body = request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect('post',pk=post.id)
    context = {'post':post,'comments':comments, 'participants':participants}
    return render(request, 'community/post.html', context)

@login_required(login_url='user_login')
def createPost(request):
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Post.objects.create(
            author=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('community')
    context = {'form':form,'topics':topics}
    return render(request, 'community/post_form.html', context)

@login_required(login_url='user_login')
def updatePost(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    topics = Topic.objects.all()
    if request.user != post.author:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        post.name = request.POST.get('name')
        post.topic = topic
        post.description = request.POST.get('description')
        post.save()
        return redirect('community')
    context = {'form':form,'topics': topics, 'post': post}
    return render(request, 'community/post_form.html', context)

@login_required(login_url='user_login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('You are not allowed here.')
    if request.method == 'POST':
        post.delete()
        return redirect('community')
    return render(request, 'community/delete.html', {'obj':post})


@login_required(login_url='user_login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse('You are not allowed here.')
    if request.method == 'POST':
        comment.delete()
        return redirect('community')
    return render(request, 'community/delete.html', {'obj':comment})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    comments = Comment.objects.all()
    return render(request, 'base/activity.html', {'comments': comments})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    comments = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'posts': posts,
               'comments': comments, 'topics': topics}
    return render(request, 'base/profile.html', context)
