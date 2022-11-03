from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from django.contrib import messages
from tkinter.tix import CheckList
from urllib import request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Challenge

# Create your views here.

def home(request):
    challenges = Challenge.objects.all()
    context = {'challenges':challenges}
    return render(request, 'index.html',context)

def challenge(request):
    # challenge = Challenge.objects.get(id=pk)
    # challenge = None
    # for i in challenges:
    #     if i['id']==int(pk):
    #       challenge=i
    # context = {'challenge':challenge}
    return render(request, './menu/challenge.html')

def calendar(request):
    return render(request, 'menu/calendar.html')

def chart(request):
    return render(request, 'menu/chart.html')

def news(request):
    return render(request, 'menu/news.html')

def user_login(request):
   
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {}
    return render(request, 'menu/login_register.html', context)


def user_logout(request):
    logout(request)
    return redirect("home")