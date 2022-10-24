from multiprocessing import context
from tkinter.tix import CheckList
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse

from .models import Challenge

# Create your views here.

def home(request):
    challenges = Challenge.objects.all()
    context = {'challenges':challenges}
    return render(request, 'index.html',context)

def challenge(request, pk):
    challenge = Challenge.objects.get(id=pk)
    # challenge = None
    # for i in challenges:
    #     if i['id']==int(pk):
    #       challenge=i
    context = {'challenge':challenge}
    return render(request, './menu/challenge.html',context)

def calendar(request):
    return render(request, 'menu/calendar.html')

def chart(request):
    return render(request, 'menu/chart.html')

def news(request):
    return render(request, 'menu/news.html')

def community(request):
    return render(request, 'menu/community.html')