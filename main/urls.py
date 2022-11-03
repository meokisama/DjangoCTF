from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('challenge',views.challenge,name="challenge"),
    path('calendar',views.calendar,name="calendar"),
    path('chart',views.chart,name="chart"),
    path('news',views.news,name="news"),
    path('user_login',views.user_login,name="user_login"),
    path('user_logout',views.user_logout,name="user_logout"),
]