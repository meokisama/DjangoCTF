from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from django.contrib import messages
from tkinter.tix import CheckList
from urllib import request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from json import dumps
from django.views.generic import ListView
from challenge.models import Challenge

from datetime import date, datetime
from django.utils import timezone
# import pandas as pd

User = get_user_model()
from community.models import Note

# Create your views here.

def home(request):
    now = timezone.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    # challenges = Challenge.objects.all()
    challenges = Challenge.objects.all().filter(date_end__gte=date,date_start__lte=date)
    context = {'challenges':challenges}
    return render(request, 'index.html',context)

# def challenge(request):
#     challenge = Challenge.objects.get(id=pk)
#     challenge = None
#     for i in challenges:
#         if i['id']==int(pk):
#           challenge=i
#     context = {'challenge':challenge}
#     return render(request, './menu/challenge.html')

def calendar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            [d,m,y]= str(request.POST.get('note_date')).split('/')
            user = User.objects.get(pk=request.user.id)
            date = y + "-" + m + "-"+ d

            if 'note_delete' in request.POST:
                try:
                    Note.objects.filter(user=user).get(date=date).delete()
                except:
                    messages.info(request, "There's not note saved")
            else:
                content = request.POST.get('note_content')
                if content != '':
                    try:
                        note = Note.objects.filter(user=user).get(date=date)
                        note.content = request.POST.get('note_content')
                    except:
                        note = Note.objects.create(user=user,date=date,content=content)
                    note.save()
                else:
                    try:
                        Note.objects.filter(user=user).get(date=date).delete()
                    except:
                        messages.info(request, "Note content can't be empty")

            return redirect('calendar')

        user = User.objects.get(pk=request.user.id)
        notes = user.note_set.all()
        dict_note = {}
        for note in notes:
            time = str(note.date).split(' ')[0]
            [year, month, day] = time.split('-')
            if month.startswith("0"):
                month = month[1]
            if day.startswith("0"):
                day = day[1]
            if "y" + year + "m" + month not in str(dict_note.keys()):
                dict_note["y" + year + "m" + month] = {}
            dict_note["y" + year + "m" + month].update({"d" + day : note.content})

        data_note = dumps(dict_note)
        content = {'data_note':data_note}
        return render(request, 'menu/calendar.html', content)
    else:
        if request.method == 'POST':
            return redirect('login')
    return render(request, 'menu/calendar.html')

def chart(request):
    return render(request, 'menu/chart.html')

def userLogin(request):
   
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST' and request.POST.get('su-username') == None:
        username = request.POST.get('username').lower()
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

    #Register Process
    if request.method == 'POST' and request.POST.get('su-username') != None:
        username = request.POST.get('su-username').lower()
        password = request.POST.get('su-password')
        email = request.POST.get('su-email')

        if User.objects.filter(username=username).exists() == False:
            user = User.objects.create_user(username,email,password)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'This username already existed')

    context = {}
    return render(request, 'menu/login_register.html', context)


def user_logout(request):
    logout(request)
    return redirect("home")

class ChallengeListView(ListView):
    model = Challenge
    context_object_name = 'object_list'
    template_name = 'index.html'
    ordering = 'date_created'
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get_queryset(self):
        now = timezone.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        queryset = Challenge.objects.filter(date_end__gte=date,date_start__lte=date,public=True)
        queryset.order_by('date_created')
        return queryset


class ChallengeListViewUpcoming(ListView):
    model = Challenge
    context_object_name = 'object_list'
    template_name = 'upcoming.html'
    ordering = 'date_created'
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get_queryset(self):
        now = timezone.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        queryset = Challenge.objects.filter(date_start__gte=date,public=True)
        queryset.order_by('date_created')
        return queryset

class ChallengeListViewExpired(ListView):
    model = Challenge
    context_object_name = 'object_list'
    template_name = 'expired.html'
    ordering = 'date_created'
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get_queryset(self):
        now = timezone.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        queryset = Challenge.objects.filter(date_end__lte=date,public=True)
        queryset.order_by('date_created')
        return queryset

class ChallengeListViewSearching(ListView):
    model = Challenge
    context_object_name = 'object_list'
    template_name = 'search.html'
    ordering = 'date_created'
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get_queryset(self):
        now = timezone.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        queryset = Challenge.objects.filter(name__contains = (self.request.GET.get('q') or ''),public=True)
        queryset.order_by('date_created')
        return queryset